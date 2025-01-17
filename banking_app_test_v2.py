import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class BankAccount:
    def __init__(self, account_holder, account_type, balance=0):
        """
        Initialize a bank account.

        :param account_holder: Name of the account holder
        :param account_type: Type of account (e.g., 'Savings', 'Checking')
        :param balance: Initial balance (default is 0)
        """
        self.account_holder = account_holder
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        """
        Deposit an amount into the account.

        :param amount: Amount to be deposited (must be positive)
        """
        if amount > 0:
            self.balance += amount
            logging.info(f"Deposited {amount}. New balance: {self.balance}")
        else:
            logging.error("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        """
        Withdraw an amount from the account.

        :param amount: Amount to be withdrawn (must be positive and less than or equal to balance)
        """
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            logging.info(f"Withdrew {amount}. New balance: {self.balance}")
        elif amount <= 0:
            logging.error("Withdrawal amount must be greater than zero.")
        else:
            logging.error("Insufficient balance!")

    def transfer(self, amount, target_account):
        """
        Transfer money from this account to another account.

        :param amount: Amount to transfer (must be positive and less than or equal to balance)
        :param target_account: Target BankAccount object to transfer money to
        """
        if isinstance(target_account, BankAccount):
            if amount <= self.balance:
                self.balance -= amount
                target_account.balance += amount
                logging.info(f"Transferred {amount} to {target_account.account_holder}. Your new balance: {self.balance}")
            else:
                logging.error("Insufficient balance to transfer.")
        else:
            logging.error("Target account is not valid.")

    def compare_balance(self, other_account):
        """
        Compare the balance of this account with another account.

        :param other_account: Another BankAccount object to compare with
        :return: String indicating whether the balance is 'larger', 'smaller', or 'equal'
        """
        if isinstance(other_account, BankAccount):
            if self > other_account:
                return "larger"
            elif self < other_account:
                return "smaller"
            else:
                return "equal"
        else:
            logging.error("Comparison account is not valid.")
            return None

    def display_account_details(self):
        """
        Display the details of the bank account.
        """
        logging.info(f"Account Holder: {self.account_holder}")
        logging.info(f"Account Type: {self.account_type}")
        logging.info(f"Balance: {self.balance}")

    def __eq__(self, other):
        """
        Equality comparison between two bank accounts based on balance.

        :param other: The other BankAccount object to compare
        :return: True if balances are equal, False otherwise
        """
        if isinstance(other, BankAccount):
            return self.balance == other.balance
        return False

    def __gt__(self, other):
        """
        Greater than comparison between two bank accounts based on balance.

        :param other: The other BankAccount object to compare
        :return: True if this account's balance is greater, False otherwise
        """
        if isinstance(other, BankAccount):
            return self.balance > other.balance
        return False

    def __lt__(self, other):
        """
        Less than comparison between two bank accounts based on balance.

        :param other: The other BankAccount object to compare
        :return: True if this account's balance is less, False otherwise
        """
        if isinstance(other, BankAccount):
            return self.balance < other.balance
        return False


# Sample CLI Application
def get_valid_account_id(accounts):
    """
    Get a valid account ID from the user.

    :param accounts: Dictionary of BankAccount objects (keyed by account ID)
    :return: Valid account ID or None if invalid
    """
    try:
        account_id = int(input("Enter account ID: "))
        if account_id in accounts:
            return account_id
        else:
            logging.error("Invalid account ID.")
            return None
    except ValueError:
        logging.error("Invalid input. Please enter a valid number.")
        return None


def get_valid_account_holder_name():
    """
    Get a valid account holder name that only contains letters.

    :return: Valid account holder name
    """
    while True:
        name = input("Enter Account Holder Name: ")
        if name.isalpha():
            return name
        else:
            logging.error("Account holder name must contain only letters. Please try again.")

def get_valid_account_type_name():
    """
    Get a valid account type name that only contains letters and numbers

    :return: Valid account type name
    """
    while True:
        name = input("Enter Account Type (Checkings, Savings): ")
        if name.isalnum():
            return name
        else:
            logging.error("Account type name must contain only letters or numbers. Please try again.")


def get_valid_balance():
    """
    Get a valid initial balance (positive number).

    :return: Valid balance
    """
    while True:
        try:
            balance = float(input("Enter initial balance: "))
            if balance >= 0:
                return balance
            else:
                logging.error("Balance must be a positive number. Please try again.")
        except ValueError:
            logging.error("Invalid input. Please enter a valid number.")


def banking_app():
    accounts = {}
    next_account_id = 1  # Start account IDs from 1

    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. View Account Details")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Compare Accounts")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            holder = get_valid_account_holder_name() 
            acc_type = get_valid_account_type_name()
            balance = get_valid_balance()  
            account = BankAccount(holder, acc_type, balance)
            accounts[next_account_id] = account
            logging.info(f"Account created for {holder} with balance {account.balance} and ID {next_account_id}")
            next_account_id += 1  

        elif choice == '2':
            if not accounts:
                logging.error("No accounts available.")
            else:
                for account_id, account in accounts.items():
                    print(f"\nAccount ID: {account_id}")
                    account.display_account_details()

        elif choice == '3':
            if not accounts:
                logging.error("No accounts available.")
            else:
                account_id = get_valid_account_id(accounts)
                if account_id is not None:
                    try:
                        amount = float(input("Enter amount to deposit: "))
                        if amount > 0:
                            accounts[account_id].deposit(amount)
                        else:
                            logging.error("Amount must be greater than zero.")
                    except ValueError:
                        logging.error("Invalid amount input.")

        elif choice == '4':
            if not accounts:
                logging.error("No accounts available.")
            else:
                account_id = get_valid_account_id(accounts)
                if account_id is not None:
                    try:
                        amount = float(input("Enter amount to withdraw: "))
                        if amount > 0:
                            accounts[account_id].withdraw(amount)
                        else:
                            logging.error("Amount must be greater than zero.")
                    except ValueError:
                        logging.error("Invalid amount input.")

        elif choice == '5':
            if len(accounts) < 2:
                logging.error("At least two accounts are required for a transfer.")
            else:
                logging.info(f"Enter your account ID followed by the account ID to transfer to")
                account_id_from = get_valid_account_id(accounts)
                account_id_to = get_valid_account_id(accounts)
                if account_id_from is not None and account_id_to is not None:
                    try:
                        amount = float(input("Enter amount to transfer: "))
                        if amount > 0:
                            accounts[account_id_from].transfer(amount, accounts[account_id_to])
                        else:
                            logging.error("Amount must be greater than zero.")
                    except ValueError:
                        logging.error("Invalid amount input.")

        elif choice == '6':
            if len(accounts) < 2:
                logging.error("At least two accounts are required for comparison.")
            else:
                account_id_1 = get_valid_account_id(accounts)
                account_id_2 = get_valid_account_id(accounts)
                if account_id_1 is not None and account_id_2 is not None:
                    comparison_result = accounts[account_id_1].compare_balance(accounts[account_id_2])
                    if comparison_result:
                        logging.info(f"The first account is {comparison_result} than the second account.")

        elif choice == '7':
            logging.info("Exiting the Banking System.")
            break

        else:
            logging.error("Invalid option. Please try again.")


if __name__ == "__main__":
    banking_app()
