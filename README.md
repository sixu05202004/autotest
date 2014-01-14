An automated management platform [Flask](http://flask.pocoo.org/)
自动化测试管理平台
===================================================================

Thanks for newsmeme at [http://flask.pocoo.org/community/poweredby/]

#Notice:
	Because this system based on hudson and hg server, so must provice hudson and hg server url in config.
	Create a task, it will create a project on hudson;
	upload code, it will decompression code package, and add all files on hg server.
	
	flask.ext.principal must be 0.3.5 or higher.
 
###Install Prerequisite:

   python setup.py install
	

###Custom the Configuration
	
	autotest/config.py

###Sync database

	python manage.py createall

###Run

	python manage.py runserver

###signup

	http://localhost:8080/account/signup/


####requirement

        'sqlalchemy-0.8.0',
        'WTForms-1.0.3',
        'twill-0.9',
        'Markdown-2.3.1',
        'Flask-0.9',
        'Flask-Cache-0.11',
        'Flask-SQLAlchemy-0.16',
        'Flask-Principal-0.3.5',
        'Flask-WTF-0.8.3',
        'Flask-Mail-0.7.6',
        'Flask-Testing-0.4',
        'Flask-Script-0.5.3',
        'Flask-Babel-0.8',
        'Flask-Uploads-0.1.3',





