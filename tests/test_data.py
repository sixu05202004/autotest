from izppy.models import User

from izppy.application import setup_app
b=setup_app()
#b.run()
a=User(username='1',email="aa@126.com",_password='123')
db.session.add(a)
db.session.commit()