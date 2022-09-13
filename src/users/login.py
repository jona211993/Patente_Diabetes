from models.entities.User import User
from run import db


def loginNormal(username, password):
    user = User.query.get(username == username)
    print("USAWEA", user)
    if user != None:
        return user
    else:
        return None
