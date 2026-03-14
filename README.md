# MusicTager

一个带有图形界面的mp3 flac元数据补全工具

## 备注
该项目原本由 [maiicy](https://github.com/Mai-icy) 创建并维护，据原项目 [Issue 3](https://github.com/Mai-icy/MusicTagger/issues/3) 声明 pillow 与 pyqt5 冲突之后，此项目没有进一步的更新。fork 此项目，使用更新的 uv 进行包管理，并使用 pyqt6 重写 UI 页面，修缮了 cloudmusic 的爬取问题。

原项目框架保持不变。 pyqt6 的改动由 claude code 完成。 cloudmusic api 修缮借用了 [pycloudmusic](https://github.com/FengLiuFeseliud/pycloudmusic) 提供的代码。

以下为原 readme. 感谢 [maiicy](https://github.com/Mai-icy) 的贡献。

## 简介 Introduction

这是基于Python3以及Pyqt5的图形界面工具，利用音乐软件api的数据，补全歌曲元数据的工具。

## 特性 Features

- 拥有方便操作的用户图形界面
- 使用了网易云，酷狗，Spotify歌曲数据
- 可以手动编辑元数据，自定义上传专辑图片
- 可以补全mp3，flac, m4a文件
- 可以下载歌词
- 可以自动补全元数据界面 Interface

## 界面 Interface

自动写入
![2](https://github.com/Mai-icy/MusicTagger/blob/main/image-folder/test.gif)
手动写入
![1](https://github.com/Mai-icy/MusicTagger/blob/main/image-folder/test2.gif)

## 运行环境与依赖 Running environment and requirements

- Python 3
- Pyqt5 module
- mutagen module
- requests module

## 联系方式 Contact

邮箱 Email：[Maiicy@foxmail.com](mailto:Maiicy@foxmail.com)

## 使用许可 Use license

[MIT](https://github.com/Mai-icy/Pixivic-crawler/blob/master/LICENSE) © Lost
