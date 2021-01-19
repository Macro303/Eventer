<img src="./logo.png" align="left" width="150" height="150" alt="Eventer Logo">

# Eventer
[![Version](https://img.shields.io/github/tag-pre/Macro303/Eventer.svg?label=version&style=flat-square)](https://github.com/Macro303/Eventer/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/Eventer.svg?style=flat-square)](https://github.com/Macro303/Eventer/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/Eventer.svg?style=flat-square)](https://github.com/Macro303/Eventer/graphs/contributors)
[![License](https://img.shields.io/github/license/Macro303/Eventer.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Using this discord bot you can add events to a Google Calendar for the below Niantic games. The bot will allow you to select specific types of events to be invited to rather than all events.  
You can invite this bot to your own server via this [link](https://discord.com/api/oauth2/authorize?client_id=738599793236115558&permissions=67464256&scope=bot)

### Calendars
*If you want the full calendar and not specific events*
 - [**Pokemon Go** Calendar](https://calendar.google.com/calendar?cid=MDZqaTEyY2tkZmVtbmFtNjJpb2MwbTZvbDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
 - [**Harry Potter: Wizards Unite** Calendar](https://calendar.google.com/calendar?cid=N2t2c2pkcGlnOHE3YWRjdmdhbzZmbTU2NmtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
 - [**Catan: World Explorers** Calendar](https://calendar.google.com/calendar?cid=cDJmMTV1djVhZW5hdTkxM3B0amk0dGJvajhAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)

## Built Using
 - [Python: 3.9.1](https://www.python.org/)
 - [pip: 20.3.3](https://pypi.org/project/pip/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)
 - [discord.py: 1.6.0](https://pypi.org/project/discord.py/)
 - [pony: 0.7.14](https://pypi.org/project/pony/)
 - [google-api-python-client: 1.12.8](https://pypi.org/project/google-api-python-client/)
 - [google-auth-httplib2: 0.0.4](https://pypi.org/project/google-auth-httplib2/)
 - [google-auth-oauthlib: 0.4.2](https://pypi.org/project/google-auth-oauthlib/)
 - [pytz: 2020.5](https://pypi.org/project/pytz/)

## Execution
1. Create a project on [Google API Console](https://console.developers.google.com/apis/dashboard), adding Google Calendar APIs to the project.
2. Create a **OAuth 2.0 Client ID** and download the `credentials.json` file.
3. Execute the following to generate the default files:
   ```bash
   $ pip install -r requirements.txt
   $ python -m Bot
   ```
4. Update the generated `config.yaml` with your Discord Token, preferred Prefix and Google Calendar ID
5. Run the following:
   ```bash
   $ python -m Bot
   ```


## Socials
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)  
 - WLG Raids & Sightings [Discord Invite](https://discord.gg/47gyFPE)
 - Wizards Unite - Wellington [Discord Invite](https://discord.gg/dy3ZhkT)
 - Catan: Wellington Explorers [Discord Invite](https://discord.gg/kFyCveQ)
