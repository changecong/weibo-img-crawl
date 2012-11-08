weibo-img-crawl
===============

Fake cookies to access weibo.cn using python, no sdk required.

## Introduction

> The code is not completed yet. It is not very efficient now.

> weibo.cn is always changed, so the code may lose functionality after couples of months. But the weibohack.py shows the base idea of how a bot sign into a website.

> The core code is in weibohack.py, file crawl.py is a web back-end program running with [webpy](http://webpy.org/). Before running the code some configuration needs to be make.

## Configuration

> webpy

>> Download webpy and extract it.
>> To use webpy, command _ln -s webpy-path/web your-crawl-python/._

> BeautifulSoup

>> Download BeautifulSoup from [here](http://www.crummy.com/software/BeautifulSoup/) and install.

> Wookmark

>> Included in /static/wookmark/ . You may also Download wookmark Jquery plug in from [here](www.wookmark.com/jquery-plugin)

> Bootstrap

>> Download [Bootstrap](http://twitter.github.com/bootstrap/), put related files into /static/

## How to
1. Run ./crawl
2. Visti http://0.0.0.0:8080 with your browser.
3. Connect weibo with your weibo account
4. Use user's uid to get their pictures.


