import random

class Db_helper():
    def temporary_password():
        hex_digits = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWQYZ')

        def hexGen():
            result = ""
            pick_from = hex_digits
            for digit in range(12):
                cur_digit = random.sample(hex_digits, 1)[0]
                result += cur_digit
                if result[-1] == cur_digit:
                    pick_from = hex_digits - set(cur_digit)
                else:
                    pick_from = hex_digits
            return result

        hex_code = hexGen()
        return hex_code
    
    # def sendEmail():
    #     return true

    # def sendingTempPass(temporaryPassword):
    #     print(Db_helper.sendEmail())