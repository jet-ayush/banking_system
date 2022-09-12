import random
import _sqlite3


class Card:
    number = None
    PIN = None

    def _init_(self):
        self.number = Luhn_Algorithm()
        self.PIN = str(format(random.randint(0000, 9999), "04d"))


def Luhn_Algorithm():
    number = "400000" + str(format(random.randint(000000000, 999999999), "09d"))
    helper = 0
    count = 0
    for x in number:
        count += 1
        if count % 2 != 1:
            helper += int(x)
        else:
            if int(x) > 4:
                helper += int(x) * 2 - 9
            else:
                helper += int(x) * 2
    return number + str(10 - helper % 10) if helper % 10 != 0 else number + "0"


def card_create():
    new_card = Card()
    print("\nYour card has been created\n"
          "Your card number:\n"
          f"{new_card.number}\n"
          "Your card PIN:\n"
          f"{new_card.PIN}\n")
    return new_card


def account_enter():
    card_number = input("\nEnter your card number:\n")
    PIN_input = input("Enter your PIN:\n")
    with conn:
        card_pin = cur.execute(f"SELECT pin FROM card WHERE number = '{card_number}';").fetchone()
    if card_pin is None or card_pin[0] != PIN_input:
        return print("\nWrong card number or PIN!\n")
    account_menu(card_number)


def account_menu(number):
    print("\nYou have successfully logged in!\n")
    while True:
        user_input = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
        if user_input == "0":
            bye()
        if user_input == "1":
            show_balance(number)
        if user_input == "2":
            add_income(number)
        if user_input == "3":
            transfer(number)
        if user_input == "4":
            delete_card(number)
            return print("\nThe account has been closed!\n")
        if user_input == "5":
            return print("\nYou have successfully logged out!\n")


def bye():
    print("\nBye!")
    exit()


def show_balance(number):
    with conn:
        balance = cur.execute(f"SELECT balance FROM card WHERE number = '{number}';").fetchone()
    return print(f"\nBalance: {balance[0]}\n")


def add_income(number):
    income = int(input("\nEnter income:\n"))
    with conn:
        cur.execute(f"UPDATE card SET balance = balance + {income} WHERE number = '{number}';")
    print("Income was added!\n")


def transfer(owner_card):
    with conn:
        money_from = cur.execute(f"SELECT balance FROM card WHERE number = '{owner_card}';").fetchone()
        money_from = money_from[0]
    stranger_card = input("\nTransfer\nEnter card number:\n")
    if stranger_card == owner_card:
        return print("You can't transfer money to the same account!\n")
    if not check_Luhn(stranger_card):
        return print("Probably you made a mistake in the card number. Please try again!\n")
    with conn:
        stranger_balance = cur.execute(f"SELECT balance FROM card WHERE number = '{stranger_card}';").fetchone()
    if stranger_balance is None:
        return print("Such a card does not exist.\n")
    money_to = int(input("Enter how much money you want to transfer:\n"))
    if money_from - money_to < 0:
        return print("Not enough money!\n")
    with conn:
        cur.execute(f"UPDATE card SET balance = balance - {money_to} WHERE number = '{owner_card}'")
        cur.execute(f"UPDATE card SET balance = balance + {money_to} WHERE number = '{stranger_card}'")
    return print("Success!\n")


def check_Luhn(card):
    control = card[-1]
    check = card[:-1]
    count = 0
    helper = 0
    for x in check:
        count += 1
        if count % 2 != 1:
            helper += int(x)
        else:
            if int(x) > 4:
                helper += int(x) * 2 - 9
            else:
                helper += int(x) * 2
    helper += int(control)
    return True if helper % 10 == 0 else False


def delete_card(number):
    with conn:
        return cur.execute(f"DELETE FROM card WHERE number = '{number}'")


if _name_ == "_main_":
    conn = _sqlite3.connect('card.s3db')
    with conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
        )
    user_card = None
    while True:
        main_input = input("1. Create an account\n2. Log into account\n0. Exit\n")
        if main_input == "0":
            bye()
        if main_input == "1":
            user_card = card_create()
            with conn:
                cur.execute(f"INSERT INTO card (number, pin) VALUES ('{user_card.number}', '{user_card.PIN}');")
        if main_input == "2":
            account_enter()