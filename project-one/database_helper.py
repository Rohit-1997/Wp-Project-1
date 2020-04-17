from models import *

# this class inserts the data into the db instance passed
class DB_Helper:
    def __init__(self,db_instance):
        self.db = db_instance

    def add_record(self,form):
        """
        add record into the databse instance
        """
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        self.db.session.add(user)
        self.db.session.commit()
