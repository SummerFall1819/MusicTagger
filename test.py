from pycloudmusic import Music163Api

import requests

api = Music163Api()

_song_info_url = 'http://music.163.com/api/song/detail/?id={}&ids=[{}]'

def get_song_info(song_id: str):
    """
    Get filtered song information based on song ID in CloudMusic API.

    :param song_id: song ID in API.
    :return: Filtered song information in dict.
    """
    res_json = requests.post(_song_info_url.format(song_id, song_id), timeout=4).json()
    if res_json['code'] == 400 or res_json['code'] == 406:
        raise requests.RequestException("访问过于频繁或接口失效")
    song_json = res_json['songs'][0]
    print(song_json)


async def _main():

    num, music_iter = await api.search_music("PHASES", limit=10)
    while True:
        try:

            item = next(music_iter)
            print(item)

            song_data = {
                "idOrMd5": str(item.id),
                "songName": "".join(item.name),
                "singer": item.artist[0]["name"],
                "duration": '%d:%d%d' % (item.duration // 60, item.duration % 60 // 10, item.duration % 10),
            }
            print(song_data)

        except StopIteration:
            print("?")
            break  # 正常迭代结束
        except Exception as e:
            print(e)
            continue






if __name__ == "__main__":
    import asyncio
    asyncio.run(_main())