from unittest import TestCase
from db_config import MongoDb
config = MongoDb('email@example.com', '12345', 'twitch_user')
config.initializingConnection()

class testingDb(TestCase):
    # test connection of mongodb, signup, login, and erorr checking with sign up 
    # and signup with same email

    def test_conn(self):
        conn = config.establishingConn()
        result = True if conn != None else False 
        self.assertEqual(result, True)

    def test_signup(self):
        config.signUp()
        successfulLogin = config.login()
        self.assertEqual(successfulLogin, True)

    def test_signup_with_same_email(self):
        emailAlreadyExists = config.signUp()
        self.assertEqual(emailAlreadyExists, False)

    def test_delete_account(self):
        config.deleteUser()
        config.username, config.password, config.twitchUsername = 'email@example.com', '12345', 'twitch_user'
        successfulLogin = config.login()
        self.assertEqual(successfulLogin, None)

    def test_signup_and_signin(self):
        config.signUp()
        successfulLogin = config.login()
        self.assertEqual(successfulLogin, True)



