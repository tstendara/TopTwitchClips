from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from emailTemplate import recoveryPassword
import smtplib, ssl
import random
import os

class Db_helper():
    def temporary_password():
        hex_digits = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWQYZ')

        def hexGen():
            result = ""
            pick_from = hex_digits
            for digit in range(random.randint(7, 13)):
                cur_digit = random.sample(hex_digits, 1)[0]
                result += cur_digit
                if result[-1] == cur_digit:
                    pick_from = hex_digits - set(cur_digit)
                else:
                    pick_from = hex_digits
            return result

        hex_code = hexGen()
        return hex_code
    
    def sendEmail(receiver, temporary_password):
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        reciever_email = receiver
        sender_email = "automaticeditor@gmail.com"
        password = os.environ['password']

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver

        part2 = MIMEText(recoveryPassword(temporary_password), "html")
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.starttls() # Secure the connection

            server.login(sender_email, password)
            server.sendmail(
                sender_email, reciever_email, message.as_string()
                )
        except Exception as e:
            print("unexpected error occured: ", e)
        finally:
            print("successfully sent")
            server.quit()

    def sendingTempPass(receiver, temporaryPassword):
        Db_helper.sendEmail(receiver ,temporaryPassword)