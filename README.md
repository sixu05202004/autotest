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





