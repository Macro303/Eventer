<img src="https://raw.githubusercontent.com/Macro303/Eventer/main/logo.png" align="left" width="120" height="120" alt="Eventer Logo">

# Eventer
[![Version](https://img.shields.io/github/tag-pre/Macro303/Eventer.svg?label=version&style=flat-square)](https://github.com/Macro303/Eventer/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/Eventer.svg?style=flat-square)](https://github.com/Macro303/Eventer/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/Eventer.svg?style=flat-square)](https://github.com/Macro303/Eventer/graphs/contributors)
[![License](https://img.shields.io/github/license/Macro303/Eventer.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Adds events to a Google Calendar, by filling out a Google Form you will be invited to all the Events of the type you select.  

## Sign Ups
 - [Catan: World Explorer](https://forms.gle/Qcc2tLpt3rSRXHuN8)
 - [Harry Potter: Wizards Unite](https://forms.gle/wwjJ1EFRxuKgZBMHA)
 - [Pokemon Go](https://forms.gle/wwjJ1EFRxuKgZBMHA)

### Calendars
*If you want the full calendar and not specific events*
 - [Catan: World Explorers](https://calendar.google.com/calendar?cid=cDJmMTV1djVhZW5hdTkxM3B0amk0dGJvajhAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
 - [Harry Potter: Wizards Unite](https://calendar.google.com/calendar?cid=N2t2c2pkcGlnOHE3YWRjdmdhbzZmbTU2NmtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)
 - [Pokemon Go](https://calendar.google.com/calendar?cid=MDZqaTEyY2tkZmVtbmFtNjJpb2MwbTZvbDRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ)

## Built Using
 - Python 3.8.2
 - PyYAML 5.3.1
 - google-api-python-client 1.9.3
 - google-auth-httplib2 0.0.4
 - google-auth-oauthlib 0.4.1
 - pytz 2020.1

## Execution
1. Create a project on [Google API Console](https://console.developers.google.com/apis/dashboard), adding both Google Sheets and Google Calendar APIs to the project.
2. Create a **OAuth 2.0 Client ID** and download the `credentials.json` file.
3. Run the following:
    ```bash
    $ pip install -r requirements.txt
    $ python -m Eventer -t
    ```
4. Edit the created `config.yaml` as needed.
5. Create `.yaml` files inside the appropriate `Events/{Game}` folder.
6. Run the following:
    ```bash
   $ python -m Eventer -cwp
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
[![Discord | Catan: Wellington Explorer](https://discord.com/api/v6/guilds/728385327294840892/widget.png?style=banner2)](https://discord.gg/kFyCveQ)
[![Discord | Wizards Unite - Wellington](https://discord.com/api/v6/guilds/577714667535728670/widget.png?style=banner2)](https://discord.gg/dy3ZhkT)
[![Discord | WLG Raids & Sightings](https://discord.com/api/v6/guilds/328347295378833408/widget.png?style=banner2)](https://discord.gg/47gyFPE)
