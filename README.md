# Tama Voices
Tools for creating voicepacks for Tama

## Dictionaries

List of available languages:

code   | language
-------|---------
**de** | German
**en** | English
**es** | Spanish
**fr** | French
**it** | Italian
**ja** | Japanese
**ko** | Korean
**pt** | Portuguese
**ru** | Russian
**zh** | Chinese

## Compilation

_tested with python 3.9.7_

```
python setup build
```

## Execution

_in compiled mode_

```
voicemaker.exe -l {lang}
```

_by running the script_

```
python main.py -l {lang} (--lv2: debug) (--lv3: trace)
```
