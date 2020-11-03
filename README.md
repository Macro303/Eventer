<img src="https://raw.githubusercontent.com/Macro303/Eventer/main/logo.png" align="left" width="150" height="150" alt="Eventer Logo">

# Eventer
[![Version](https://img.shields.io/github/tag-pre/Macro303/Eventer.svg?label=version&style=flat-square)](https://github.com/Macro303/Eventer/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/Eventer.svg?style=flat-square)](https://github.com/Macro303/Eventer/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/Eventer.svg?style=flat-square)](https://github.com/Macro303/Eventer/graphs/contributors)
[![Visits](https://badges.pufler.dev/visits/Macro303/Eventer?style=flat-square)](https://badges.pufler.dev)
[![License](https://img.shields.io/github/license/Macro303/Eventer.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Adds events to a Google Calendar, by filling out a Google Form you will be invited to all the Events of the type you select.

## Sign Ups
 - [**Pokemon Go** form](https://forms.gle/PFGsN4YyugzMFmWT7)
 - [**Harry Potter: Wizards Unite** form](https://forms.gle/wFTtK4pWhUJ5HBp36)
 - [**Catan: World Explorer** form](https://forms.gle/9FTx2hdgKxmEgPDs6)

### Calendars
*If you want the full calendar and not specific events*
 - [**Pokemon Go** calendar](https://calendar.google.com/calendar?cid=MDZqaTEyY2tkZmVtbmFtNjJpb2MwbTZvbDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
 - [**Harry Potter: Wizards Unite** calendar](https://calendar.google.com/calendar?cid=N2t2c2pkcGlnOHE3YWRjdmdhbzZmbTU2NmtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
 - [**Catan: World Explorers** calendar](https://calendar.google.com/calendar?cid=cDJmMTV1djVhZW5hdTkxM3B0amk0dGJvajhAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)

## Built Using
 - [Python: 3.8.5](https://www.python.org/)
 - [pip: 20.2.4](https://pypi.org/project/pip/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)
 - [google-api-python-client: 1.12.5](https://pypi.org/project/google-api-python-client/)
 - [google-auth-httplib2: 0.0.4](https://pypi.org/project/google-auth-httplib2/)
 - [google-auth-oauthlib: 0.4.2](https://pypi.org/project/google-auth-oauthlib/)
 - [pytz: 2020.4](https://pypi.org/project/pytz/)

## Execution
1. Create a project on [Google API Console](https://console.developers.google.com/apis/dashboard), adding both Google Sheets and Google Calendar APIs to the project.
2. Create a **OAuth 2.0 Client ID** and download the `credentials.json` file.
3. Run the following:
   ```bash
   $ pip install -r requirements.txt
   $ python -m Calendar -t
   ```
4. Edit the created `config.yaml` as needed.
5. Create `.yaml` files inside the appropriate `Events/{Game}` folder.
6. Run the following:
   ```bash
   $ python -m Calendar -cwp
   ```

## Arguments
*You can find all these by using the `-h` or `--help` argument*

| Game | Short | Long |
| ---- | ----- | ---- |
| Catan: World Explorers | `-c` | `--catan` |
| Harry Potter: Wizards Unite | `-w` | `--wizards` |
| Pokemon Go | `-p` | `--pokemon` |

Running with the `-t` or `--test` argument will not create the Google Calendar Events


## Socials
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)  
 - WLG Raids & Sightings [Discord Invite](https://discord.gg/47gyFPE)
 - Wizards Unite - Wellington [Discord Invite](https://discord.gg/dy3ZhkT)
 - Catan: Wellington Explorers [Discord Invite](https://discord.gg/kFyCveQ)
