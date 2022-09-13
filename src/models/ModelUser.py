from .entities.User import User
from run import db


class ModelUser():

    @classmethod
    def loginA(self, dbA, user):
        try:
            cursor = dbA.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(
                    row[2], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self, username, password):
        try:
            user = User.query.get(username == username)

            if user != None:
                if(user.password == password):
                    return user
                else:
                    return 1
            else:
                return 1
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(
                id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
