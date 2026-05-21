#!/usr/bin/python
# -*- coding:utf-8 -*-

import asyncio
import io
import re
import time
from typing import List

import requests
from PIL import Image
from pycloudmusic import Music163Api

from api.api_error import NoneResultError
from lyric_decode.lyric_decode import LrcFile
from song_metadata.metadata_type import SongInfo, SongSearchInfo


class CloudMusicWebApi:
    def __init__(self):
        self._song_info_url = "http://music.163.com/api/song/detail/?id={}&ids=[{}]"
        self._download_lrc_url = "http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1&rv=-1"
        self.api = Music163Api()

    def get_song_info(self, song_id: str) -> SongInfo:
        res_json = requests.post(self._song_info_url.format(song_id, song_id), timeout=4).json()
        if res_json["code"] in (400, 406):
            raise requests.RequestException("CloudMusic API request was rejected")

        song_json = res_json["songs"][0]
        artists_list = [info["name"] for info in song_json["artists"]]
        duration = song_json["duration"] // 1000

        pic_url = song_json["album"]["picUrl"]
        pic_response = requests.get(pic_url, timeout=4)
        pic_response.raise_for_status()
        with Image.open(io.BytesIO(pic_response.content)) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.thumbnail((500, 500))

            pic_buffer = io.BytesIO()
            img.save(pic_buffer, format="JPEG", quality=85)
            pic_buffer.seek(0)

        lrc_file = self.get_lrc(song_id)
        lyric = lrc_file.get_content("non") or ""

        song_info = {
            "singer": ",".join(artists_list),
            "songName": song_json["name"],
            "album": song_json["album"]["name"],
            "year": str(time.localtime(song_json["album"]["publishTime"] // 1000).tm_year),
            "trackNumber": (song_json["no"], song_json["album"]["size"]),
            "duration": f"{duration // 60}:{duration % 60 // 10}{duration % 10}",
            "genre": None,
            "picBuffer": pic_buffer,
            "lyric": lyric,
        }
        return SongInfo(**song_info)

    async def _search_data(self, keyword: str, page: int = 0) -> List[SongSearchInfo]:
        keyword = re.sub(r"[!@#$%^&*/]+", "", keyword).strip()
        if not keyword:
            raise NoneResultError

        res_json = await self.api._search(keyword, type_=1, page=page, limit=20)
        result = res_json.get("result") or {}
        songs = result.get("songs") or []
        if result.get("songCount", 0) == 0 or not songs:
            raise NoneResultError

        res_list = []
        for data in songs:
            song_id = data.get("id")
            song_name = data.get("name")
            if song_id is None or not song_name:
                continue

            duration = int(data.get("dt") or data.get("duration") or 0) // 1000
            artists = data.get("ar") or data.get("artists") or []
            artist_names = [
                artist.get("name", "")
                for artist in artists
                if artist.get("name")
            ]
            song_data = {
                "idOrMd5": str(song_id),
                "songName": song_name,
                "singer": ",".join(artist_names),
                "duration": f"{duration // 60}:{duration % 60 // 10}{duration % 10}",
            }
            res_list.append(SongSearchInfo(**song_data))

        if not res_list:
            raise NoneResultError
        return res_list

    def search_data(self, keyword: str, page: int = 0) -> List[SongSearchInfo]:
        return asyncio.run(self._search_data(keyword, page))

    def get_lrc(self, song_id: str) -> LrcFile:
        res_json = requests.get(self._download_lrc_url.format(song_id), timeout=4).json()
        lrc_file = LrcFile()
        if res_json.get("lrc"):
            lrc_file.load_content(res_json["lrc"].get("lyric", ""), "non")
        if res_json.get("tlyric"):
            lrc_file.load_content(res_json["tlyric"].get("lyric", ""), "chinese")
        if res_json.get("romalrc"):
            lrc_file.load_content(res_json["romalrc"].get("lyric", ""), "romaji")
        return lrc_file


if __name__ == "__main__":
    pass
