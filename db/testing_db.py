import unittest
from db_config import MongoDb

config = MongoDb('email@example.com', 'newpassword', 'twitch_user')
config.initializingConnection()

class testingDb(unittest.TestCase):
    # test connection of mongodb, signup, login, and erorr checking with sign up 
    # and signup with same email, and resetting password

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
        config.username, config.password, config.twitchUsername = 'email@example.com', 'newPassword', 'twitch_user'
        successfulLogin = config.login()
        self.assertEqual(successfulLogin, None)

    def test_signup_and_signin(self):
        config.signUp()
        successfulLogin = config.login()
        self.assertEqual(successfulLogin, True)

    def test_changing_password(self):
        temporaryPassword = config.sendingRecoveryPassword()
        if temporaryPassword:
            email = config.recoveryEmail(temporaryPassword)
            if email:
                config.resettingPassword(email, 'newpassword')
                self.assertEqual(True, True)
            else:
                self.assertEqual(print(email), 'Didnt get back email needed to reset password | There was a problem finding the temporary password in makingVideos.recoveryAccount')
        else:
            self.assertEqual(print(temporaryPassword), 'Didnt get back temporary password | check to see if testing env var exists and is = True and make sure that email exits already')
        

if __name__ == "__main__":
    unittest.main()

