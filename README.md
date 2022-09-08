# Tama Voices

<img src="https://user-images.githubusercontent.com/6703996/189178570-0909bd95-ad55-4ef0-bbe8-f379b8991096.png" height="100" />

Tools for creating voicepacks for Tama

## Dictionaries

List of available languages:

code   | language | code   | language
-------|----------|--------|---------
**de** | German   |**ja**  | Japanese
**en** | English  |**ko**  | Korean
**es** | Spanish  |**pt**  | Portuguese
**fr** | French   |**ru**  | Russian
**it** | Italian  |**zh**  | Chinese

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
