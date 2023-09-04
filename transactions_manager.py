class TransactionsManager():
    # tables: Transactions ATMTransactions
    # transactions columns: TransactionID	FromAccountNumber	ToAccountNumber	TransactionType	TransactionDate	Amount	Description
    # ATMTransactions columns: TransactionID	CustomerID	TransactionType	TransactionDate	Amount	ATMLocation

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def getTransactions(self, AccountNumber):
        self.cursor.execute(
            "SELECT * FROM Transactions WHERE FromAccountNumber = ?", (AccountNumber,))
        result = self.cursor.fetchall()
        return result

    def getATMTransactions(self, CustomerID):
        self.cursor.execute(
            "SELECT * FROM ATMTransactions WHERE CustomerID = ?", (CustomerID,))
        result = self.cursor.fetchall()
        return result

    def addTransaction(self, FromAccountNumber, ToAccountNumber, TransactionType, TransactionDate, Amount, Description):
        insert_query = """
            INSERT INTO Transactions (
                FromAccountNumber,
                ToAccountNumber,
                TransactionType,
                TransactionDate,
                Amount,
                Description
            ) VALUES (?, ?, ?, ?, ?, ?)
            """
        new_transaction_data = (
            FromAccountNumber,
            ToAccountNumber,
            TransactionType,
            TransactionDate,
            Amount,
            Description
        )

        self.cursor.execute(insert_query, new_transaction_data)
        self.conn.commit()
        return (True, "Transaction successful.")

    def addATMTransaction(self, CustomerID, TransactionType, TransactionDate, Amount, ATMLocation):
        insert_query = """
            INSERT INTO ATMTransactions (
                CustomerID,
                TransactionType,
                TransactionDate,
                Amount,
                ATMLocation
            ) VALUES (?, ?, ?, ?, ?)
            """
        new_transaction_data = (
            CustomerID,
            TransactionType,
            TransactionDate,
            Amount,
            ATMLocation
        )

        self.cursor.execute(insert_query, new_transaction_data)
        self.conn.commit()
        return (True, "Transaction successful.")
