#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
    helpers.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from threading import Thread
from hashlib import md5
import redis
import socket


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@async
def clear(host, port, db):
    redis.StrictRedis(host=host, port=port, db=db).flushdb()


access = {100: "public",
          300: "private"}

role = {100: "memeber",
        200: "MODERATOR",
        300: "admin"}

result = {0: "success",
          1: "fail"}

hudson = {1: "running",
          2: "invalid",
          3: "disable",
          4: "enable"}


def get_access(id):
    return access.get(id)


def get_role(id):
    return role.get(id)


def get_result(id):
    return result.get(id)


def get_hudson(id):
    return hudson.get(id)


def make_userid(cookie, area='00', id="310000"):
    userid = area + id + cookie
    return md5(userid).hexdigest()[:16].upper()


def make_ua(ua):
    ua_md5 = md5(ua).hexdigest()
    return (ua_md5[24] + ua_md5[25] + ua_md5[16] + ua_md5[17] +
            ua_md5[8] + ua_md5[9] + ua_md5[0] + ua_md5[1]).upper()


def make_userid_ua(ip, ua, area="00", id="100000"):
    userid = area + id + ip + ua
    return md5(userid).hexdigest()[:16].upper()


def ip_to(IP='255.255.255.255'):
    IP1 = IP.split('.')[0]
    IP2 = IP.split('.')[1]
    IP3 = IP.split('.')[2]
    IP4 = IP.split('.')[3]
    a = int(IP1) * 256 ** 3 + \
        int(IP2) * 256 ** 2 + \
        int(IP3) * 256 + \
        int(IP4)
    num = socket.htonl(a)
    return num

if __name__ == '__main__':
    print make_userid(cookie='ABCD',area='00',id="320000")