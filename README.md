## Overview
Web config interface for Raspberry PI Camplayer: https://github.com/raspicamplayer/camplayer

Originally, camplayer can only be configured via an ini config file which is a little tedious.
This provides a friendly UI to add, edit and delete video channels, with templates for most common IP camera brands (hikvision and dahua).

Access at `http://<rpi-ip>:8080` (rpi-ip could be localhost or 192.168.1.xxx depending on where you want to access it from)

## Requirements
- Install camplayer according to repo: https://github.com/raspicamplayer/camplayer
- While the streamlit server could work pretty much anywhere\*, it's only useful where camplayer itself is installed - which only works on Raspbian OS due to omxplayer dependency on the specific Broadcom GPU.
- Working python3 installation.

\* *As of writing this, streamlit can't run as-is on arm32v7 / armhf architecture (such as raspberry pi 3) because it depends on pyarrow which is virtually impossible to compile on this arch. However, pyarrow is not (yet) a hard dependency of streamlit, therefore we can use a clever trick and mock it. This is achieved by installing all streamlit dependencies except pyarrow, and then do some magic to avoid failing the import of pyarrow. See `src/streamlit_no_pyarrow.py` for details.*

## Installation
- `git clone https://github.com/dorinclisu/camplayer_streamlit.git`
- `cd camplayer_streamlit && sudo ./install.sh`

## TODO
- Basic authentication
- Threading locks (when saving config files)


## Screenshots
![home](https://user-images.githubusercontent.com/13818396/222974026-4dfe394f-8d88-4793-849a-379d25c580d2.png)
![add](https://user-images.githubusercontent.com/13818396/222974019-588bf106-34a2-4295-a7ff-86addfdfcdea.png)
![update](https://user-images.githubusercontent.com/13818396/222974027-ae3b1f9e-dbc5-4c58-8cfe-ad2d072a85c0.png)
![update_override](https://user-images.githubusercontent.com/13818396/222974031-307b711d-4e6f-4bd2-9be4-b91140824d1c.png)
![display](https://user-images.githubusercontent.com/13818396/222974023-bb23cac6-4ef7-4657-a37a-a38743792941.png)
