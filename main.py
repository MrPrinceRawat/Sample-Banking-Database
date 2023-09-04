from db_manager import DBManager
from user_manager import UserManager, LoginManager
from transactions_manager import TransactionsManager
from designs import BANK_NAME, colors
from datetime import datetime
import getpass

conn, cursor = DBManager('sample_bank.db').connect()
user_manager = UserManager(conn)
login_manager = LoginManager(conn)
transactions_manager = TransactionsManager(conn)


bank_name_normal = "QuantumBankX"

default_options = [
    "1. Create Account",
    "2. Create Login",
    "3. Login",
    "4. Exit"
]

account_options = [
    "1. Deposit",
    "2. Withdraw",
    "3. Transfer",
    "4. Mini Recipt",
    "5. Logout"
]

login_requirements = [
    "1. CustomerID",
    "2. Password",
]

create_account_requirements = [
    "1. First Name",
    "2. Last Name",
    "3. Date of Birth(YYYY-MM-DD)",
    "4. Gender(M/F)",
    "5. Address",
    "6. Phone Number",
    "7. Email",
    "8. Account Type(Savings/Current)"
]

create_login_requirements = [
    "1. CustomerID",
    "2. Password",
    "3. Confirm Password"
]


if __name__ == '__main__':
    print(BANK_NAME)
    print(colors.bold, colors.fg.cyan, "Welcome to QuantumBankX", colors.reset)
    while True:
        current_user = None
        print("Please select an option:")
        for option in default_options:
            print(option)
        option = input("Enter option: ")
        if option == "1":
            data = []
            for requirement in create_account_requirements:
                data.append(input(requirement + ": "))
            status = user_manager.createUser(data[0], data[1], data[2], data[3], data[4],
                                             data[5], data[6], data[7])
            if status[0]:
                print(colors.fg.green, "Account created successfully.", colors.reset)
                print("CustomerID: " + str(status[2]))
                print("Account Number: " + str(status[3]))
                print()
            else:
                print(colors.fg.red, status[1], colors.reset)
        elif option == "2":
            data = []
            for requirement in create_login_requirements:
                data.append(input(requirement + ": "))
            if data[1] != data[2]:
                print(colors.fg.red, "Passwords do not match.", colors.reset)
                continue
            login_manager.createLogin(data[0], data[1])
            print(colors.fg.green, "Login created successfully.", colors.reset)
            print()
        elif option == "3":
            data = []
            for requirement in login_requirements:
                data.append(input(requirement + ": "))
            login_result = login_manager.login(data[0], data[1])
            if login_result[0]:
                print(colors.fg.green, "Login successful.", colors.reset)
                current_user = user_manager.getUserByCustomerID(data[0])
                print("Welcome, " + current_user[1] + " " + current_user[2])
            else:
                print(colors.fg.red, login_result[1], colors.reset)
        elif option == "4":
            exit()
        else:
            print(colors.fg.red, "Invalid option.", colors.reset)
            continue
        while current_user:
            print("Please select an option:")
            for option in account_options:
                print(option)
            option = input("Enter option: ")
            if option == "1":
                amount = input("Enter amount to deposit: ")
                user_manager.updateBalance(current_user[0], amount)
                transactions_manager.addTransaction(
                    current_user[0], current_user[0], "Deposit", datetime.now(), amount, "Deposit")
                print(colors.fg.green, "Deposit successful.", colors.reset)
                print()
            elif option == "2":
                amount = input("Enter amount to withdraw: ")
                status = user_manager.updateBalance(
                    current_user[0], -int(amount))
                if not status[0]:
                    print(colors.fg.red, status[1], colors.reset)
                    print()
                    continue
                transactions_manager.addTransaction(
                    current_user[0], current_user[0], "Withdraw", datetime.now(), amount, "Withdraw")
                print("Withdrawal successful.")
            elif option == "3":
                amount = input("Enter amount to transfer: ")
                to_account_number = input(
                    "Enter account number to transfer to: ")
                status = user_manager.updateBalance(
                    current_user[0], -int(amount))
                if status[0]:
                    transactions_manager.addTransaction(
                        current_user[8], to_account_number, "Transfer", datetime.now(), amount, "Transfer")
                    to_user = user_manager.getUser(to_account_number)
                    user_manager.updateBalance(to_user[0], amount)
                    print(colors.fg.green, "Transfer successful.", colors.reset)
                else:
                    print(colors.fg.red, status[1], colors.reset)
            elif option == "4":
                print()
                balance = user_manager.getCurrentBalance(current_user[8])
                print("Current Balance: " + str(balance))
                print("Transactions:")
                transactions = transactions_manager.getTransactions(
                    current_user[8])
                for transaction in transactions:
                    print(transaction)
                print("ATM Transactions:")
                atm_transactions = transactions_manager.getATMTransactions(
                    current_user[8])
                for atm_transaction in atm_transactions:
                    print(atm_transaction)
                print()
            elif option == "5":
                print("Logging out.")
                current_user = None
            else:
                print("Invalid option.")
                continue
