#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

"""
    config.py
    ~~~~~~~~~~~

    autotest basic configuration

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""


class defaultconfig():
    # debug mole
    DEBUG = True
    '''
    # configuration mysql--- for test
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % \
        ('root', 'root', '10.0.2.53', 'autotest')

    '''
    # configuration mysql--- for prodict
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % \
        ('root', 'root', '10.0.2.53', 'izppy')

    # the secret key
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #SECRET_KEY = "secret"

    # flask extension mail debug
    MAIL_DEBUG = DEBUG

    # mail address
    MAILHOST = 'mail.autotest.com'
    MAIL_SERVER = 'mail.autotest.com'
    DEFAULT_MAIL_SENDER = 'mailtest@autotest.com'
    MAIL_DEFAULT_SENDER = 'mailtest@autotest.com'
    MAIL_USERNAME = 'mailtest'
    MAIL_PASSWORD = 'yvtg45h5'
    DEFAULT_MAIL_RECEIVER = "dd@autotest.com"
    MAIL_RECEIVER = ["dd@autotest.com"]
    MAIL_SUBJECT = "Fatal: Task: %s  fail num: %s! Please check task manage web, thanks!"
    MAIL_BODY = "Please check: http://10.0.2.205:8080/task/%s/showstat_name/, thanks!"
    #lan
    ACCEPT_LANGUAGES = ['en', 'zh', 'en_gb']

    # log
    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

    # cache configure
    CACHE_TYPE = "redis"
    CACHE_DEFAULT_TIMEOUT = 86400
    CACHE_REDIS_HOST = "10.0.2.205"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

    # upload
    #UPLOAD_FOLDER= '/home/code/'
    #UPLOADS_DEFAULT_DEST= ''
    UPLOADED_FILES_DEST = '/home/code/'

    #hudson url
    HUDSON = 'http://10.0.2.204:8080/hudson/'

    #HUDSON_START = '%(host)s/notice/start/$JOB_NAME/$BUILD_NUMBER/$BUILD_ID/'

    HUDSOM_DATA = 'python start.py -u %s/notice/$JOB_NAME/$BUILD_NUMBER/$BUILD_ID/'
    #HUDSON_END = '%(host)s/notice/end/$JOB_NAME/$BUILD_NUMBER/$BUILD_ID/'

    #log url
    LOG_URL = 'http://10.0.2.204/alllogs/'

    #code url
    CODE_URL = 'http://10.0.2.205:9090/hg/test.cgi/code/'
