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

    # configuration mysql
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % \
        ('root', 'root', '127.0.0.1', 'autotest')

    # the secret key
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #SECRET_KEY = "secret"

    # flask extension mail debug
    MAIL_DEBUG = DEBUG

    # mail address
    MAILHOST = 'mail.autotest.com'
    DEFAULT_MAIL_SENDER = 'mailtest@autotest.com'
    MAIL_USERNAME = 'mailtest@autotest.com'
    MAIL_PASSWORD = 'mailtest123'
    DEFAULT_MAIL_RECEIVER = "admin@autotest.com"

    #lan
    ACCEPT_LANGUAGES = ['en', 'zh', 'en_gb']

    # log
    DEBUG_LOG = 'logs/debug.log'
    ERROR_LOG = 'logs/error.log'

    # cache configure
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300

    # upload
    #UPLOAD_FOLDER= '/home/code/'
    #UPLOADS_DEFAULT_DEST= ''
    UPLOADED_FILES_DEST = '/home/code/'

    #hudson url
    HUDSON = 'http://127.0.0.1/hudson/'

    #HUDSON_START = '%(host)s/notice/start/$JOB_NAME/$BUILD_NUMBER/$BUILD_ID/'

    HUDSOM_DATA = 'python start.py -u %s/notice/$JOB_NAME/$BUILD_NUMBER/$BUILD_ID/'
    #HUDSON_END = '%(host)s/notice/end/$JOB_NAME/$BUILD_NUMBER/$BUILD_ID/'

    #log url
    LOG_URL = 'http://127.0.0.1/alllogs/'

    #code url
    CODE_URL = 'http://127.0.0.1/hg/test.cgi/code/'
