weibo-img-crawl
===============

use python to connect weibo.cn, no sdk required

## Introduction

> The core code is in weibohack.py, file crawl.py is a web back-end program running with [webpy](http://webpy.org/). Before running the code some configuration needs to be make.

## Configuration

> webpy

Download webpy and extract it.
To use webpy, command _ln -s webpy-path/web your-crawl-python/._

> BeautifulSoup
Download BeautifulSoup from [here](http://www.crummy.com/software/BeautifulSoup/) and install.

> Wookmark
Download wookmark Jquery plug in.

> Bootstrap
Download Bootstrap, put related files into /static/

## How to
1. Run ./crawl
2. Visti http://0.0.0.0:8080 with your browser.
3. Connect weibo with your weibo account
4. Use user's uid to get their pictures.


