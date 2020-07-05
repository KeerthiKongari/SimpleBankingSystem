import random
import sys
import sqlite3

account_mid = []
bank_accounts = {}
conn = sqlite3.connect('card.s3db')
c = conn.cursor()

card = '''
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
        );
    '''
c.execute(card)
conn.commit()


def see_card(conn):
    c = conn.cursor()
    card_query = ('SELECT * FROM card')
    c.execute(card_query)
    card = c.fetchall()
    print(card)


def new_info(conn, info):
    new = '''
    INSERT INTO card (
        id, number, pin, balance)
        VALUES(?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(new, info)
    conn.commit()


def luhn(account):
    fake = '1'
    number = fake + account
    numb_list = list(number)
    for i in range(1, len(numb_list)):
        if i % 2 != 0:
            x = int(numb_list[i])
            x = 2 * x
            numb_list[i] = str(x)
    for i in range(1, len(numb_list)):
        x = int(numb_list[i])
        if x > 9:
            x = x - 9
            numb_list[i] = str(x)
    numb_list.pop(0)
    total = 0
    for i in range(len(numb_list)):
        x = int(numb_list[i])
        total += x
    if total % 10 == 0:
        return '0'
    else:
        goal = (round(total + 5, -1))
        return str(goal - total)


def new_account(account_mid, bank_accounts):
    iin = '400000'
    account = str(random.randint(100000000, 1000000000))
    p = 0
    while p == 0:
        if account in account_mid:
            account = str(random.randint(100000000, 1000000000))
            p = 0
        else:
            account_mid.append(account)
            p = 1
    account = iin + account
    checksum = luhn(account)
    account_number = account + checksum
    pin = str(random.randint(1000, 10000))
    balance = 0
    info = (1, account_number, pin, 0)
    new_info(conn, info)

    bank_accounts[account_number] = [pin, balance]
    print()
    print('Your card has been created')
    print('Your card number:')
    print(account_number)
    print('Your card PIN:')
    print(pin)
    print()
    menu(account_mid, bank_accounts)


def log_in(bank_accounts, conn):
    def balance(conn, customer):
        if type(customer) == str:
            c = conn.cursor()
            numbers_query = ('SELECT * FROM card WHERE number = ?')
            c.execute(numbers_query, (customer,))
            user = c.fetchone()
            return user
        c = conn.cursor()
        numbers_query = ('SELECT * FROM card WHERE number = ?')
        c.execute(numbers_query, (customer[1],))
        user = c.fetchone()
        return user

    def verification(bank_accounts, conn):
        n = 0
        while n == 0:
            print('Enter your card number:')
            # card_number = '4000005448089079'
            card_number = input()
            print('Enter your PIN: ')
            # card_pin = '2037'
            card_pin = input()
            c = conn.cursor()
            numbers_query = ('SELECT * FROM card WHERE number = ?')
            c.execute(numbers_query, (card_number,))
            user = c.fetchone()
            if user == None:
                print('Wrong card number or PIN!')
                menu(account_mid, bank_accounts)
            if card_pin == user[2]:
                print('You have successfully logged in')
                n = 1
            else:
                print('Wrong card number or PIN!')
                menu(account_mid, bank_accounts)

        return user

    def add_money(customer, income, conn):
        account_info = balance(conn, customer)
        total = account_info[3]
        new_balance = (income + total)
        person = account_info[1]
        balance_update = (new_balance, person)
        balance_query = 'UPDATE card SET balance = ? WHERE number = ?'
        c.execute(balance_query, balance_update)
        conn.commit()
        user = balance(conn, customer)
        if user[3] == new_balance:
            return True

    def transfer(conn, customer):
        print('Transfer')
        print('Enter card number:')
        destination = input()
        temp = destination[0:-1]
        luhn_last = luhn(temp)
        last = destination[-1]
        if luhn_last != last:
            print('Probably you made mistake in the card number. Please try again!')
            return False
        recepient = balance(conn, destination)
        if recepient == None:
            print('Such a card does not exist.')
            return False
        print('Enter how much money you want to transfer:')
        change = int(input())
        depositer_balance = balance(conn, customer)
        if depositer_balance[3] < change:
            print('Not enough money!')
            return False
        if add_money(recepient, change, conn) == True and add_money(depositer_balance, -1 * change, conn) == True:
            print('Success!')

    def closure(conn, customer):
        account = customer[1]
        c.execute("DELETE FROM card WHERE number = ?", (account,))
        conn.commit()
        c.close()
        print("The account has been closed!")

    customer = verification(bank_accounts, conn)
    p = 0
    while p == 0:
        print(
            '''        
            1. Balance
            2. Add income
            3. Do transfer
            4. Close account
            5. Log out
            0. Exit
            ''')
        step = int(input())
        if step == 1:
            user = balance(conn, customer)
            print(f'Balance: {user[3]}')
            p = 0
        if step == 2:
            income = int(input('Enter income: '))
            success = add_money(customer, income, conn)
            if success == True:
                print('Income was added!')
        if step == 3:
            transfer(conn, customer)
            p = 0
        if step == 4:
            closure(conn, customer)
            menu(account_mid, bank_accounts)
        if step == 5:
            print('You have successfully logged out!')
            menu(account_mid, bank_accounts)
        if step == 29:
            see_card(conn)
            p = 0
        if step == 0:
            conn.close()
            print('Bye')
            sys.exit()
    else:
        print('Wrong card number or PIN!')
        menu(account_mid, bank_accounts)


def menu(account_mid, bank_accounts):
    print(
        '''
        1. Create an account
        2. Log into account
        0. Exit
        ''')
    choice = int(input())
    if choice == 1:
        new_account(account_mid, bank_accounts)
    if choice == 2:
        log_in(bank_accounts, conn)
    if choice == 29:
        see_card(conn)
        p = 0
    if choice == 0:
        conn.close()
        print('Bye!')
        sys.exit()


menu(account_mid, bank_accounts)
