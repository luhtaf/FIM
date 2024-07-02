# Introduction
This program is File Integrity Monitoring, that make scan your file periodically, then detect if there are creation, modification, or deletion of files in directory

# Requirement

## Make Telegram Bot API
Go to  [Telegram Core](https://core.telegram.org/api/obtaining_api_id) and make api key for your apps


## Install Pip and library
First, install pip 
* in ubuntu:

    `sudo apt install python3-pip`
* in centos:

    `yum install python3-pip`

then install requirements with pip
* in linux:

    `pip install -r requirements.txt`

* in windows:

    `python3 -m pip install -r requirements.txt`

# Running
fill config in `fim_config.yaml` and run:

    `python3 custom_fim.py`

# Addition
if u already have FIM with `elasticagent` or `auditbeat` you can use `FIM_Elastic_to_Telegram.py` instead to notif FIM log to telegram:

    `python3 FIM_Elastic_to_Telegram.py`