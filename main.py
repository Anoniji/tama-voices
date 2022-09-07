#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created by Anoniji
Library made available under the terms of the license
Creative Commons Zero v1.0 Universal
https://creativecommons.org/publicdomain/zero/1.0/

get data from aspell
aspell -d en dump master | aspell -l en expand > en.txt
"""

import os
import sys
import argparse
import shutil
import sqlite3
import logging
from logger import Logger

from gtts import gTTS
from pydub import AudioSegment, effects
import soundfile as sf
import numpy as np


def sep_sys():
    if sys.platform == 'win32':
        return r'\\'
    return '/'


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter('array', convert_array)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lang', type=str)
    parser.add_argument('-e', '--encoding', type=str, default='utf-8')
    args, unknown = parser.parse_known_args()
    lang = args.lang
    encoding = args.encoding

    # init logger
    logger = Logger()
    logger.log_nms = 'voicemaker'
    if '--lv2' not in unknown:
        logging.disable(logging.CRITICAL)

    if lang:

        # Variables
        dictionaries_path = '.' + sep_sys() + 'dictionaries' + sep_sys() + lang + '.txt'
        temps_dir = '.' + sep_sys() + '.temps' + sep_sys()
        voicepack_dir = '.' + sep_sys() + 'voices' + sep_sys()
        voicepack_path = voicepack_dir + lang + '.vpdb'
        s_strip = [15, -15]
        octaves = {'fr': 0.35, 'en': 0.35, 'ja': 0.25}
        vo_rate = {'fr': 1.07, 'en': 1.07, 'ja': 1.00}

        if os.path.isfile(dictionaries_path):
            if not os.path.isdir(voicepack_dir):
                logger.prt('info', 'Creation of the output folder', 2)
                os.mkdir(voicepack_dir)

            if not os.path.isdir(temps_dir):
                logger.prt('info', 'Creation of the temps folder', 2)
                os.mkdir(temps_dir)

            conn = sqlite3.connect(voicepack_path)
            cur = conn.cursor()
            logger.prt('info', 'Connected to database', 2)

            lines = open(dictionaries_path, encoding=encoding).readlines()
            lines_len = len(lines)
            logger.prt('info', 'Dictionary ' + lang + ' loaded (' + str(lines_len) + ' words)', 1)

            index = 0
            for word in lines:
                index += 1
                word = word.upper().strip()
                schema = word[0]

                logger.prt('info', 'schema: ' + schema + ' | words: ' + word, 3)

                # TTS
                tts = gTTS(word, lang=lang)
                tts.save(temps_dir + 'temps.mp3')
                logger.prt('sucess', 'step 1: generate', 2)

                # Clear
                audio = AudioSegment.from_mp3(temps_dir + 'temps.mp3')
                lst = np.array(audio.get_array_of_samples())

                cnt, stp, array = ([0, 0], [False, False], [])
                for point in lst:
                    array.append(point)

                for pos in range(0, 2):
                    for point in array:
                        if not stp[pos] and point >= s_strip[1] and point <= s_strip[0]:
                            cnt[pos] = cnt[pos] + 1

                        elif not stp[pos] and point < s_strip[1] or point > s_strip[0]:
                            stp[pos] = True

                        else:
                            array.reverse()

                audio = audio._spawn(lst[cnt[0]:-cnt[1]])
                logger.prt('sucess', 'step 2: clear', 2)

                # Export
                audio.export(temps_dir + 'temps.wav', format='wav')
                logger.prt('sucess', 'step 3: export', 2)

                # Change rate
                data, samplerate = sf.read(temps_dir + 'temps.wav')
                samplerate = int(samplerate * vo_rate[lang])
                sf.write(temps_dir + 'temps.wav', data, samplerate)
                logger.prt('sucess', 'step 4: change rate', 2)

                # Change octave
                sound = AudioSegment.from_file(temps_dir + 'temps.wav', format='wav')
                data, rate = sf.read(temps_dir + 'temps.wav')
                f_rate = int(sound.frame_rate * (2.0 ** octaves[lang]))
                n_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': f_rate})
                n_sound = n_sound.set_frame_rate(rate)
                n_sound.export(temps_dir + 'temps.mp3', format='mp3')
                logger.prt('sucess', 'step 5: change octave', 2)

                # Normalize
                audio = AudioSegment.from_mp3(temps_dir + 'temps.mp3')
                audio = effects.normalize(audio)
                logger.prt('sucess', 'step 6: normalize', 2)

                # Export
                audio.export(temps_dir + 'temps.wav', format='wav')
                logger.prt('sucess', 'step 7: export', 2)

                # DB
                cur.execute(
                    'SELECT data FROM ' + schema + ' WHERE kt=?',
                    (word,))

                get_data = cur.fetchone()
                if not get_data:
                    a = AudioSegment.from_mp3(temps_dir + 'temps.mp3')
                    y = np.array(a.get_array_of_samples())
                    if a.channels == 2:
                        y = y.reshape((-1, 2))

                    sql = 'INSERT INTO ' + schema + '''(kt,data)
                              VALUES(?,?) '''
                    cur = conn.cursor()
                    task = (word, y)
                    cur.execute(sql, task)
                    conn.commit()

                    logger.prt('sucess', 'added to database', 1)
                else:
                    logger.prt('sucess', 'already present', 2)

                sys.exit(0)

            if os.path.isdir(temps_dir):
                logger.prt('info', 'Creation of the temps folder', 2)
                shutil.rmtree(temps_dir)

        else:
            logger.prt('info', 'Dictionary not found')

    else:
        logger.prt('info', 'Please set --lang parameter')
