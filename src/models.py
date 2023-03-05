from enum import Enum
from typing import Literal
from typing import get_args
from urllib.parse import urlparse

from pydantic import BaseModel



class DeviceBrand(str, Enum):
    hikvision = 'HIKVISION'
    dahua     = 'dahua'

    @classmethod
    def options(cls):
        return list(map(lambda c: c.value, cls))


class ChannelStream(BaseModel):
    brand: DeviceBrand = DeviceBrand.hikvision
    host:          str = ''
    port:          int = 554
    ch:            int = 1
    hd:           bool = False
    user:          str = ''
    passwd:        str = ''
    url:           str = ''

    def get_url(self) -> str:
        if self.url:
            result = urlparse(self.url)

            if not result.password:
                netloc = f'{self.user}:{self.passwd}@{result.hostname}'
                if result.port:
                    netloc = f'{netloc}:{result.port}'

                result = result._replace(netloc=netloc)

            return result.geturl()

        if self.brand == DeviceBrand.hikvision:
            channel = f'{self.ch}{"01" if self.hd else "02"}'
            return f'rtsp://{self.user}:{self.passwd}@{self.host}:{self.port}/Streaming/Channels/{channel}'

        if self.brand == DeviceBrand.dahua:
            subtype = '0' if self.hd else '1'
            return f'rtsp://{self.user}:{self.passwd}@{self.host}:{self.port}/cam/realmonitor?channel={self.ch}&subtype={subtype}'

        raise TypeError(f'Unknown brand {self.brand}')

    def get_url_masked(self) -> str:
        url = self.get_url()
        result = urlparse(url)
        if result.password:
            return url.replace(result.password, '***')
        return url


class Channel(BaseModel):
    name:              str
    preview: ChannelStream
    detail:  ChannelStream


WindowCount = Literal[1,4,6,7,8,9,10,13,16]


class Config(BaseModel):
    channels:  list[Channel] = []
    count:       WindowCount = get_args(WindowCount)[0]
    layout:        list[str] = []
    ini_path:            str = '~/.camplayer/config.ini'

    def get_channel_names(self) -> list[str]:
        return list(map(lambda ch: ch.name, self.channels))
