import sqlite3


class DBManager():
    def __init__(self, name):
        self.name = name

    def connect(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS AccHolders(CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,FirstName TEXT NOT NULL,LastName TEXT NOT NULL,DateOfBirth DATE,Gender CHAR(1),Address TEXT,PhoneNumber TEXT,Email TEXT,AccountNumber INTEGER UNIQUE,AccountType TEXT,Balance DECIMAL(10, 2),DateOpened DATE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS transactions (TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,FromAccountNumber INTEGER NOT NULL,ToAccountNumber INTEGER NOT NULL,TransactionType TEXT NOT NULL,TransactionDate TIMESTAMP NOT NULL,Amount DECIMAL(10, 2) NOT NULL,Description TEXT,FOREIGN KEY (FromAccountNumber) REFERENCES AccHolders(AccountNumber),FOREIGN KEY (ToAccountNumber) REFERENCES AccHolders(AccountNumber));")
        cursor.execute("CREATE TABLE IF NOT EXISTS ATMTransactions (TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,CustomerID INTEGER NOT NULL,TransactionType TEXT NOT NULL,TransactionDate TIMESTAMP NOT NULL,Amount DECIMAL(10, 2) NOT NULL,ATMLocation TEXT NOT NULL,FOREIGN KEY (CustomerID) REFERENCES AccHolders(CustomerID));")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Logins (CustomerID INTEGER PRIMARY KEY,PasswordHash TEXT NOT NULL,FOREIGN KEY (CustomerID) REFERENCES AccHolders(CustomerID));")
        return (conn, cursor)
