# Hucking e-diary

This script:
- update all schoolkid's marks less then '4' for '5',
- remove all schoolkid's chastisements,
- add random commendation for random last subject in schoolkid's schedule,
- limit number of commendations (for 15) by removing old commendations

## How to install

Clone scripts.py to your local device. To avoid problems with installing required additinal packages, use a virtual environment, for example:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

Python3.12 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

The script doesnt uses additinal packages:

_Django==5.2.*_

_isoweek==1.3.*_

_environs==14.2.*_

After that you can run script using this command:

```bash
python scripts.py
```

Its possible to run script with schoolkid's name you need adding argument in console like:

```bash
python scripts.py --full_name 'schoolkid's name'
```


## Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org.


