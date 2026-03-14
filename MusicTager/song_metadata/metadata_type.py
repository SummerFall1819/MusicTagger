#!/usr/bin/python
# -*- coding:utf-8 -*-
# Origin author: Mai-icy.
import collections
from dataclasses import dataclass

@dataclass
class SongInfo:
    singer: str
    songName: str
    album: str
    year: str
    trackNumber: str
    duration: str
    genre: str
    picBuffer: bytes
    lyric: str

@dataclass
class SongElseInfo:
    songPath: str
    suffix: str
    coverName: str
    createTime: str
    modifiedTime: str
    md5: str

@dataclass
class SongSearchInfo:
    songName: str
    singer: str
    duration: str
    idOrMd5: str

SongInfo = collections.namedtuple("SongInfo",
                                  ["singer",
                                   "songName",
                                   "album",
                                   "year",
                                   "trackNumber",
                                   "duration",
                                   "genre",
                                   "picBuffer",
                                   "lyric"])

SongElseInfo = collections.namedtuple(
    "SongElseInfo", [
        "songPath", "suffix", "coverName", "createTime", "modifiedTime", "md5"])


SongSearchInfo = collections.namedtuple(
    "SongSearchInfo", [
        "songName", "singer", "duration", "idOrMd5"])
