#!/usr/bin/python
# -*- coding:utf-8 -*-
# Origin author: Mai-icy.
import io
import os
import time
import hashlib
from pathlib import Path
from typing import Tuple

import mutagen
from mutagen.flac import FLAC
from pymediainfo import MediaInfo
from song_metadata.metadata_type import SongInfo, SongElseInfo
from tinytag import TinyTag


def get_md5(file: str) -> str:
    """获取文件的md5值"""
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    return md5code


def get_album_buffer(path: Path) -> io.BytesIO:
    """获取文件的封面数据，并保存到io缓冲"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}', can't get pic buffer.")
    buffer = io.BytesIO()

    match path.suffix:
        case '.mp3':
            inf = mutagen.File(path)
            artwork = b''
            if not inf.tags:
                return buffer
            for i in inf.tags:
                if i[:5] == 'APIC:':
                    artwork = inf.tags[i].data
            if not artwork:
                return buffer
            buffer.write(artwork)
        case '.flac':
            audio = FLAC(path)
            if len(audio.pictures) == 0:
                return buffer
            else:  # flac可以有多个图片，这里只读取一个
                buffer.write(audio.pictures[-1].data)
        case __:
            return buffer



def read_song_metadata(path: str) -> Tuple[SongInfo, SongElseInfo]:
    """获取文件的元数据"""
    path:Path = Path(path)
    audio = mutagen.File(path)
    tag = TinyTag.get(path)
    # meta data.
    suffix = path.suffix
    file_name = path.name
    state_info = path.stat()
    create_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(state_info.st_birthtime))
    modified_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(state_info.st_mtime))
    duration = tag.duration
    if path.suffix in ['.m4a', '.mp4']:
        media = MediaInfo.parse(path)
        duration = round(media.tracks[0].duration / 1000)
    # pic buffer
    pic_buffer = get_album_buffer(path)
    # lyrics
    lyric = ""
    if suffix == '.mp3' and audio.tags:
        uslt_tag = audio.tags.getall('USLT::XXX')
        if uslt_tag:
            lyric = uslt_tag[0].text
    elif suffix == '.flac' and 'LYRICS' in audio:
        lyric = audio['LYRICS'][0]

    text_duration = f"{duration // 60}:{duration % 60 // 10}{duration % 10}"
    song_info_dict = {
        "singer": tag.artist,
        "songName": tag.title,
        "album": tag.album,
        "genre": tag.genre,
        "year": tag.year,
        "trackNumber": tag.track,
        "picBuffer": pic_buffer,
        "duration": text_duration,
        "lyric": lyric
    }
    else_info = {
        "songPath": path,
        "suffix": suffix,
        "coverName": None,
        "createTime": create_time,
        "modifiedTime": modified_time,
        "md5": get_md5(path)
    }
    if len(file_name.split(' - ')) == 2:
        if not song_info_dict['songName']:
            song_info_dict['songName'] = file_name.split(' - ')[1]
        if not song_info_dict['singer']:
            song_info_dict['singer'] = file_name.split(' - ')[0]
    return SongInfo(**song_info_dict), SongElseInfo(**else_info)


if __name__ == '__main__':
    pass
    # print(read_song_metadata(path))

