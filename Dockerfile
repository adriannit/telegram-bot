FROM python:3
ADD hass.py /
ADD qbittorrent.py /
ADD main.py /
RUN pip3 install python-telegram-bot homeassistant-api qbittorrent-api 
CMD [ "python3", "./main.py" ]
