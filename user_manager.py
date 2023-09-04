from datetime import datetime
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class UserManager():
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def createUser(self, FirstName, LastName, DateOfBirth, Gender,	Address, PhoneNumber,	Email, AccountType):
        self.cursor.execute("SELECT MAX(AccountNumber) FROM AccHolders")
        result = self.cursor.fetchone()
        # Check if there are existing account numbers
        highest_account_number = result[0] if result[0] is not None else 100000
        AccountNumber = highest_account_number + 1
        CreationDate = datetime.today().strftime("%Y-%m-%d")
        insert_query = """
            INSERT INTO AccHolders (
                FirstName,
                LastName,
                DateOfBirth,
                Gender,
                Address,
                PhoneNumber,
                Email,
                AccountNumber,
                AccountType,
                Balance,
                DateOpened
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        new_user_data = (
            FirstName,
            LastName,
            DateOfBirth,
            Gender,
            Address,
            PhoneNumber,
            Email,
            AccountNumber,
            AccountType,
            1000.00,
            CreationDate
        )
        self.cursor.execute(insert_query, new_user_data)
        self.conn.commit()
        user = self.getUser(AccountNumber)
        return (True, user, user[0], AccountNumber)

    def deleteUser(self, AccountNumber):
        delete_query = """
            DELETE FROM AccHolders WHERE CustomerID = ?
            """
        self.cursor.execute(delete_query, (AccountNumber,))
        self.conn.commit()
        return (True, "User deleted successfully.")

    def getUser(self, AccountNumber):
        self.cursor.execute(
            "SELECT * FROM AccHolders WHERE AccountNumber = ?", (AccountNumber,))
        result = self.cursor.fetchone()
        return result

    def getUserByCustomerID(self, CustomerID):
        self.cursor.execute(
            "SELECT * FROM AccHolders WHERE CustomerID = ?", (CustomerID,))
        result = self.cursor.fetchone()
        return result

    def getCurrentBalance(self, AccountNumber):
        self.cursor.execute(
            "SELECT Balance FROM AccHolders WHERE AccountNumber = ?", (AccountNumber,))
        result = self.cursor.fetchone()
        return result[0]

    def updateBalance(self, CustomerID, Amount):
        self.cursor.execute(
            "SELECT Balance FROM AccHolders WHERE CustomerID = ?", (CustomerID,))
        result = self.cursor.fetchone()
        newBalance = result[0] + int(Amount)
        if newBalance < 0:
            return (False, "Insufficient funds.")
        query = """
            UPDATE AccHolders SET Balance = ? WHERE CustomerID = ?
            """
        self.cursor.execute(query, (newBalance, CustomerID))
        self.conn.commit()
        return (True, "Balance updated successfully.")


class LoginManager():
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def login(self, CustomerID, Password):
        self.cursor.execute(
            "SELECT * FROM Logins WHERE CustomerID = ? ", (CustomerID))
        result = self.cursor.fetchone()
        if result is None:
            return (False, "User does not exist.")
        else:
            storedPasswordHash = result[1]
            if storedPasswordHash == hash_password(Password):
                return (True, "Login successful.")
            else:
                return (False, "Incorrect password.")

    def changePassword(self, CustomerID, Password):
        self.cursor.execute(
            "SELECT * FROM Logins WHERE CustomerID = ? ", (CustomerID))
        result = self.cursor.fetchone()
        if result is None:
            return (False, "User does not exist.")
        else:
            query = """
                UPDATE Logins SET PasswordHash = ? WHERE CustomerID = ?
                """
            self.cursor.execute(query, (hash_password(Password), CustomerID))
            self.conn.commit()
            return (True, "Password changed successfully.")

    def createLogin(self, CustomerID, Password):
        query = """
            INSERT INTO Logins (CustomerID, PasswordHash) VALUES (?, ?)
            """
        self.cursor.execute(query, (CustomerID, hash_password(Password)))
        self.conn.commit()
        return (True, "Login created successfully.")
