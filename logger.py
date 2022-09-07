#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created by Anoniji
Library made available under the terms of the license
Creative Commons Zero v1.0 Universal
https://creativecommons.org/publicdomain/zero/1.0/
"""

import os
import sys
import datetime
import glob
import zipfile
from colorama import init, Fore, Style
init()


def sep_sys():
    if sys.platform == 'win32':
        return r'\\'
    return '/'


class Logger:

    """Lib logger manage
    - init list: log_nms, logs_dir, level, save
    - def list: index_file, save_on_file, params, logprt
    """

    def __init__(self):
        self.log_nms = 'logger'
        self.logs_dir = '.' + sep_sys() + '.logs'
        self.level = 1
        self.save = True

        if '--lv2' in sys.argv:
            self.level = 2

        elif '--lv3' in sys.argv:
            self.level = 3

        if os.name == 'nt':
            os.system('')


    def index_file(self):
        """Indexer module
        """
        if os.path.isdir(self.logs_dir):
            try:
                cwd = os.getcwd()
                os.chdir(self.logs_dir + sep_sys())
                now = str(datetime.datetime.now())[:-7].split(' ')[0]
                files_list = glob.glob('*.log')
                for file in files_list:
                    if now not in file:
                        fl_dt = file.split('_')[-1][:-4]
                        with zipfile.ZipFile(fl_dt + '_logs.zip', 'a') as log_zip:
                            log_zip.write(file)

                        os.remove(file)

                os.chdir(cwd)
                return True

            except Exception:
                os.chdir(cwd)
                return False

        return False

    def save_on_file(self, line):
        """Logger module

        Keyword arguments:
        line [str] -- line
        """
        if not os.path.isdir(self.logs_dir):
            os.mkdir(self.logs_dir)

        log_file = open(self.logs_dir + sep_sys() + self.log_nms + '_' + str(
            datetime.datetime.now())[:-7].split(' ')[0] + ".log", mode="a+", encoding="utf-8")
        log_file.write(line + '\n')
        log_file.close()

    def params(self, key):
        """Return color list (Default UNDERLINE)
        - var list: HEADER, INFO, OK, WARNING, FAIL, END, BOLD, UNDERLINE
        """
        values = {
            'INFO': Style.BRIGHT + Fore.CYAN,
            'OK': Style.BRIGHT + Fore.GREEN,
            'WARNING': Style.BRIGHT + Fore.YELLOW,
            'FAIL': Style.BRIGHT + Fore.RED,
            'DEFAULT': Style.BRIGHT + Fore.WHITE,
            'END': Style.RESET_ALL,
        }
        return values.get(key, Style.RESET_ALL)

    def prt(self, typ, text, lv=1):
        """Logger module

        Keyword arguments:
        typ [str] -- log type
        text [str] -- text to display
        lv [int] -- log level: info(1) debug(2) trace(3)
        """
        if typ == 'info':
            color = self.params('INFO')
        elif typ == 'warning':
            color = self.params('WARNING')
        elif typ == 'error':
            color = self.params('FAIL')
        else:
            color = self.params('OK')

        return_txt = '[' + str(datetime.datetime.now())[:-3] + '] '
        return_txt += '[' + color + typ.capitalize().ljust(7) + self.params('END') + '] '
        return_txt += '[' + self.params('DEFAULT') + self.log_nms.ljust(10) + self.params('END') + '] '
        return_txt += color + str(text) + self.params('END')

        if self.level >= lv:
            print(return_txt)

        if self.save:
            self.save_on_file('[' + str(
                datetime.datetime.now())[:-3] + '] [' + typ.capitalize().ljust(7) + '] ' + str(
                text))
