import random

def Lunh_algo():
    while True:
        val = random.randint(4000000000000000, 4000009999999999)
        y = list(str(val))
        total = 0
        for num in range(0, 15):
            if num % 2 == 0:
                x = int(y[num]) * 2
                y[num] = str(x)
        for num in range(0, 15):
            if int(y[num]) > 9:
                x = int(y[num]) - 9
                y[num] = str(x)
        for num in range(0, 15 + 1):
            total += int(y[num])
            y[num] = int(y[num])
        if total % 10 == 0:
            return val
            break
        else:
            continue

def card_verify(val):
    v = val
    y = list(str(v))
    total = 0
    for num in range(0, 15):
        if num % 2 == 0:
            x = int(y[num]) * 2
            y[num] = str(x)
    for num in range(0, 15):
        if int(y[num]) > 9:
            x = int(y[num]) - 9
            y[num] = str(x)
    for num in range(0, 15 + 1):
        total += int(y[num])
        y[num] = int(y[num])
    if total % 10 == 0:
        return "yes"
    else:
        return "no"

class CreditCard:
    accout_number = 0
    pin = 0
    def __init__(self):
        self.account_number = Lunh_algo()
        self.pin = f"{random.randint(0000, 9999):04}"
        self.balance = 0

    def __repr__(self):
        return f"{self.account_number}"


while True:
    choice = input("1. Create an account \n"
                   "2. Log into account \n"
                   "0. Exit")

    if choice == "1":
        credit_card = CreditCard()
        print(f"""Your card has been created
Your card number:
{credit_card.account_number}
Your card PIN:
{credit_card.pin}""")
    elif choice == "2":
        card_number = input("Enter your card number:")
        pin_number = input("Enter your PIN:")
        res = card_verify(card_number)
        if res == "no" and card_number != credit_card.account_number or pin_number != credit_card.pin:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            while True:
                login_choice = input("""1. Balance
2. Log out
0. Exit""")
                if login_choice == "1":
                    print("Balance:", credit_card.balance)
                elif login_choice == "2":
                    print("You have successfully logged out!")
                    break
                else:
                    exit()
    else:
        print("Bye!")
        break
