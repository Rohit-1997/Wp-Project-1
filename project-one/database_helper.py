"""
    This is a helper class to help with
    regular DB operations
"""
class DB_Helper:
    def __init__(self,db_instance,table):
        self.db = db_instance
        self.table = table

    def add_record(self,form):
        """
        add record into the databse instance
        """
        user = self.table(username=form.username.data, email=form.email.data, password=form.password.data)
        self.db.session.add(user)
        self.db.session.commit()

    def query_records(self):
        """
        This method queries all the records present in the table
        """
        data = self.table.query.all()
        return data
