import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class User:
    def __init__(self, name, contact_info):
        """Represents a user in the banking system."""
        if self.validate_name(name):
            self.name = name
        else:
            raise ValueError("Name must contain only letters.")

        if self.validate_email(contact_info):
            self.contact_info = contact_info
        else:
            raise ValueError("Invalid email address.")

    @staticmethod
    def validate_email(email):
        """Validates an email address."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_name(name):
        """Validates that the name contains only letters."""
        return name.isalpha()

    def display_user_details(self):
        logging.info(f"User Name: {self.name}")
        logging.info(f"Contact Info: {self.contact_info}")

class Account:
    def __init__(self, user, account_type, balance=0):
        """Represents an individual bank account."""
        self.user = user
        if self.validate_account_type(account_type):
            self.account_type = account_type
        else:
            raise ValueError("Account type must contain only letters and numbers.")
        self.balance = round(balance, 2)

    @staticmethod
    def validate_account_type(account_type):
        """Validates that the account type contains only letters and numbers."""
        return account_type.isalnum()

    def deposit(self, amount):
        if amount > 0:
            self.balance += round(amount, 2)
            logging.info(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        else:
            logging.error("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= round(amount, 2)
            logging.info(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        elif amount <= 0:
            logging.error("Withdrawal amount must be greater than zero.")
        else:
            logging.error("Insufficient balance!")

    def transfer(self, amount, target_account):
        if isinstance(target_account, Account):
            if amount > 0 and amount <= self.balance:
                self.balance -= round(amount, 2)
                target_account.balance += round(amount, 2)
                logging.info(f"Transferred ${amount:.2f} to {target_account.user.name}. Your new balance: ${self.balance:.2f}")
            else:
                logging.error("Insufficient balance to transfer.")
        else:
            logging.error("Target account is not valid.")

    def compare_balance(self, other_account):
        if isinstance(other_account, Account):
            logging.info(f"Your balance: ${self.balance:.2f}")
            logging.info(f"Other account balance: ${other_account.balance:.2f}")
            balance_diff = abs(self.balance - other_account.balance)
            if self.balance > other_account.balance:
                logging.info(f"Your account has ${balance_diff:.2f} more than the other account.")
            elif self.balance < other_account.balance:
                logging.info(f"Your account has ${balance_diff:.2f} less than the other account.")
            else:
                logging.info("Both accounts have the same balance.")
        else:
            logging.error("Invalid account for comparison.")

    def display_account_details(self):
        logging.info(f"Account Holder: {self.user.name}")
        logging.info(f"Account Type: {self.account_type}")
        logging.info(f"Balance: ${self.balance:.2f}")

class Bank:
    def __init__(self):
        """Represents the banking system."""
        self.accounts = {}
        self.registered_emails = set()
        self.next_account_id = 1

    def create_account(self, name, contact_info, account_type, initial_balance):
        if contact_info in self.registered_emails:
            logging.error("This email is already in use. Please use a different email.")
            return None

        user = User(name, contact_info)
        account = Account(user, account_type, round(initial_balance, 2))
        account_id = self.next_account_id
        self.accounts[account_id] = account
        self.registered_emails.add(contact_info)  # Add email to the set
        self.next_account_id += 1
        logging.info(f"Account created for {name} with ID {account_id} and balance ${initial_balance:.2f}")
        return account_id

    def get_account(self, account_id):
        return self.accounts.get(account_id)

    def display_all_accounts(self):
        if not self.accounts:
            logging.error("No accounts available.")
        for account_id, account in self.accounts.items():
            logging.info(f"\nAccount ID: {account_id}")
            account.display_account_details()

# Utility Functions
def get_valid_input(prompt, validation_func):
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        logging.error("Invalid input. Please try again.")

def get_positive_float(prompt):
    return get_valid_input(prompt, lambda x: x.replace('.', '', 1).isdigit() and float(x) >= 0)

def banking_app():
    bank = Bank()

    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. View Account Details")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Compare Balances")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = get_valid_input("Enter account holder name: ", User.validate_name)
            contact_info = get_valid_input("Enter contact info (valid email): ", User.validate_email)
            account_type = get_valid_input("Enter account type (letters and numbers only): ", Account.validate_account_type)
            initial_balance = float(get_positive_float("Enter initial balance: "))
            account_id = bank.create_account(name, contact_info, account_type, initial_balance)
            if account_id:
                logging.info(f"Account successfully created with ID: {account_id}")

        elif choice == '2':
            bank.display_all_accounts()

        elif choice == '3':
            account_id = int(get_valid_input("Enter account ID: ", lambda x: x.isdigit()))
            account = bank.get_account(account_id)
            if account:
                amount = float(get_positive_float("Enter amount to deposit: "))
                account.deposit(amount)
            else:
                logging.error("Account not found.")

        elif choice == '4':
            account_id = int(get_valid_input("Enter account ID: ", lambda x: x.isdigit()))
            account = bank.get_account(account_id)
            if account:
                amount = float(get_positive_float("Enter amount to withdraw: "))
                account.withdraw(amount)
            else:
                logging.error("Account not found.")

        elif choice == '5':
            from_account_id = int(get_valid_input("Enter your account ID: ", lambda x: x.isdigit()))
            to_account_id = int(get_valid_input("Enter target account ID: ", lambda x: x.isdigit()))

            from_account = bank.get_account(from_account_id)
            to_account = bank.get_account(to_account_id)

            if from_account and to_account:
                amount = float(get_positive_float("Enter amount to transfer: "))
                from_account.transfer(amount, to_account)
            else:
                logging.error("One or both accounts not found.")

        elif choice == '6':
            account_id_1 = int(get_valid_input("Enter first account ID: ", lambda x: x.isdigit()))
            account_id_2 = int(get_valid_input("Enter second account ID: ", lambda x: x.isdigit()))

            account_1 = bank.get_account(account_id_1)
            account_2 = bank.get_account(account_id_2)

            if account_1 and account_2:
                account_1.compare_balance(account_2)
            else:
                logging.error("One or both accounts not found.")

        elif choice == '7':
            logging.info("Exiting the Banking System.")
            break

        else:
            logging.error("Invalid choice. Please try again.")

if __name__ == "__main__":
    banking_app()
