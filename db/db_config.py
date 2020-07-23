from pymongo import MongoClient
from bson.objectid import ObjectId
from db_helpers import Db_helper
import datetime
import os

class MongoDb(Db_helper):
    # This class is for connecting to the mongoDb instance and is responsible for
    # all core functions such as logging in, signing up, recovery password.
    # 
    # Current Database info:
    # makingVideos.posts - User account information
    # makingVideos.recoveryAccount - Temporary passwords

    def __init__(self, email, password, twitchUsername):
        Db_helper.__init__(self)
        self.username = email
        self.password = password
        self.twitchUsername = twitchUsername
        self.conn = None
        self.db = None

    def establishingConn(self):
        conn = MongoClient('localhost', 27017)

        if conn is None:
            return conn
        else:
            return conn

    def initializingConnection(self):
        conn = self.establishingConn()
        if conn == None:
            return None
        else:
            self.conn, client = conn, conn
        
        db = client['makingVideos']
        self.db = db

    def dupEmail(self):
        posts = self.db.posts
        result = posts.find_one({"email": self.username})
        print(result)
        output = True if result != None else None

        return output

    # returns True if login is successful
    def login(self):
        posts = self.db.posts
        result = posts.find_one({"email": self.username, "pass": self.password})
        output = True if result != None else None
        return output

    # returns success statement if account wasnt used
    def signUp(self):
        # check to see if proper email when input isnt focused on anymore
        checkingEmail = self.dupEmail()
        userExists = True if checkingEmail == None else False

        if userExists:
            return self.storeAccount() == 'successfully made account!'
        else:
            return False

    def deleteUser(self):
        posts = self.db.posts
        posts.delete_one({"email": self.username, "pass": self.password})
        self.username, self.password, self.twitchUsername = None, None, None
        
    def storeAccount(self):
        posts = self.db.posts
        post = {"email": self.username, "pass": self.password, "twitchusername": self.twitchUsername}
        posts.insert_one(post)
        return 'successfully made account!'

    def sendingRecoveryPassword(self):
        posts = self.db.posts
        # Email should exist in db
        emailExists = posts.find_one({'email': self.username})

        if emailExists:
            client = self.db
            db = client['recoveryAccount']
            temporaryPassword = Db_helper.temporary_password()
            now = datetime.datetime.utcnow()

            # creating document to hold temp_password for account recovery with and expiration time of 2 min -> (https://docs.mongodb.com/manual/tutorial/expire-data/)
            db.insert_one({"createdAt": now, "logEvent": 2, "temp_pass": temporaryPassword, "email": self.username})
            # Once user enters email to send temp password to then the page will change
            # to a verification input awaiting the users temporary password
            testing = True if "testing" in os.environ else False
            
            if testing:
                return temporaryPassword
            else:
                # send email with temporaryPassword and email in order to find account information 
                Db_helper.sendingTempPass(self.username, temporaryPassword)
        else:
            return 'no account with that email was found'

    def recoveryEmail(self, temporaryPass):
        # findout if temporary pass matches temporary password in makingVideos.recoveryAccount collection 
        client = self.db
        db = client['recoveryAccount']

        tempInfo = db.find_one({"temp_pass": temporaryPass})

        if tempInfo:
            email = tempInfo['email']
            return email
        else:
            return None

    def resettingPassword(self, email, newPassword):    
        client = self.db
        db = client['posts']
        userInformation = db.find_one({"email": email})

        userInformation['pass'] = newPassword
        db.save(userInformation)
        
    def gettingAllUsers(self):
        # Will be used to get all users, and start making videos
        return True
