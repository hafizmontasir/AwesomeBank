"""
AwesomeGIC Bank - Simple Banking System
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List
import re

class Transaction:
    """Represent a bank transaction"""

    def __init__(self, date: str, account: str, txn_type: str, amount: Decimal, txn_id: str =""):
        self.date = date
        self.account = account
        self.txn_type = txn_type.upper()
        self.amount = amount
        self.txn_id = txn_id
        
    def __str__(self):
        txn_id_display = self.txn_id if self.txn_id else ""
        return f"| {self.date} | {txn_id_display:11} | {self.txn_type:2} | {self.amount:7.2f} |"

##################################### Test Class Transaction ####################################################

# deposit = Transaction("20230601", "AC001", "D", Decimal("100.00"), "20230601-01")
# withdrawal = Transaction("20230615", "AC001", "w", Decimal("50.00"), "20230615-01")

# print(deposit)
# print(withdrawal)

################################################## end ########################################################

class InterestRule:
    """Represent an interest rule"""
    
    def __init__(self, date: str, rule_id: str, rate: Decimal):
        self.date = date
        self.rule_id = rule_id
        self.rate = rate
        
    def __str__(self):
        return f"| {self.date} | {self.rule_id:6} | {self.rate:8.2f} |"

######################################### Example usage of class InterestRule ################################################
# rule1 = InterestRule("20230101", "RULE01", Decimal("1.95"))
# rule2 = InterestRule("20230615", "SUMMER", Decimal("2.20"))

# print(rule1)
# print(rule2)

################################################ end ##################################################

class Account:
    """Rpresent an bank account"""
    
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.transactions: List[Transaction] = []
        self.balance = Decimal('0')
        
    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the account"""
        if transaction.txn_type == 'W':
            if self.balance < transaction.amount:
                raise ValueError("Insufficient balance for withdrawal")
            self.balance -= transaction.amount
        elif transaction.txn_type in ['D', 'I']:
            self.balance += transaction.amount
        
        self.transactions.append(transaction)
        
    def get_balance_at_date(self, target_date: str) -> Decimal:
        """Get account balance at end of specific date"""
        balance = Decimal('0')
        for transaction in self.transactions:
            if transaction.date <= target_date:
                if transaction.txn_type == 'W':
                    balance -= transaction.amount
                else:
                    balance += transaction.amount
        return balance
    
####################################### Example usage of class Account ####################################
# account = Account("AC001")

# account.add_transaction(Transaction("20230101", "AC001", "D", Decimal("100.00")))
# account.add_transaction(Transaction("20230115", "AC001", "W", Decimal("50.00")))

# print(account.balance)

# print(account.get_balance_at_date("20230110"))

################################################ end ##################################################

class BankingSystem:
    """main banking system class"""

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.interest_rules: List[InterestRule] = []
        self.transaction_counters: Dict[str, int] = {}
    
    def validate_date(self, date_str: str) -> bool:
        """Validate date format YYYYMMDD"""
        if not re.match(r'^\d{8}$', date_str):
            return False
        try:
            datetime.strptime(date_str, '%Y%m%d')
            return True
        except ValueError:
            return False
    
    def validate_amount(self, amount_str: str) -> bool:
        """validate amount format"""
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                return False
            if amount.as_tuple().exponent < -2:
                return False
            return True
        except:
            return False
    
    def generate_transaction_id(self, date: str) -> str:
        """Generate unique transaction ID"""
        if date not in self.transaction_counters:
            self.transaction_counters[date] = 0
        self.transaction_counters[date] += 1
        return f"{date}-{self.transaction_counters[date]:02d}"

    def input_transaction(self, input_line: str) -> str:
        """Process transaction input"""
        parts = input_line.strip().split()
        if len(parts) != 4:
            return "Invalid format. Expected: <Date> <Account> <Type> <Amount>"
        date, account, txn_type, amount_str = parts
        
        if not self.validate_date(date):
            return "Invalid format. Use YYYYMMDD"
        
        if txn_type.upper() not in ['D','W']:
            return "Invalid transaction type. Use D for depositt or W for withdrawal"
        
        if not self.validate_amount(amount_str):
            return "Invalid amount, Must be positive with max 2 decimal places"    
        
        amount = Decimal(amount_str)
        txn_type = txn_type.upper()

        if account not in self.accounts:
            if txn_type == 'W':
                return "Cannot withdraw from new account with zero balance"
            self.accounts[account] = Account(account)
        
        if txn_type == 'W' and self.accounts[account].balance < amount:
            return "Insufficient balance for withdrawal"
        
        txn_id = self.generate_transaction_id(date)
        transaction = Transaction(date, account, txn_type, amount, txn_id)
        
        self.accounts[account].add_transaction(transaction)
        return self.get_account_statement(account)
    
    def define_interest_rule(self, input_line: str) -> str:
        """Process interest rule input"""
        parts  = input_line.strip().split()
        if len(parts) != 3:
            return "Invalid format. Expected: <Date> <RuleId> <Rate in %>"
        
        date, rule_id, rate_str = parts
        
        if not self.validate_date(date):
            return "Invalid date format. Use YYYYMMDD"

        try:
            rate = Decimal(rate_str)
            if rate <= 0 or rate >= 100:
                return "Interest rate must be between 0 and 100"
        except:
            return "Invalid rate format"
        
        self.interest_rules = [rule for rule in self.interest_rules if rule.date != date]

        new_rule = InterestRule(date, rule_id, rate)
        self.interest_rules.append(new_rule)

        self.interest_rules.sort(key=lambda x: x.date)
        return self.get_interest_rules_display()
    
    def get_account_statement(self, account: str) -> str:
        """Get account statement without interest"""
        if account not in self.accounts:
            return f"Account {account} not found"
        
        acc = self.accounts[account]
        result = [f"Account: {account}"]
        result.append("| Date     | Txn Id      |Type| Amount  |")

        for transaction in acc.transactions:
            result.append(str(transaction))
        
        return "\n".join(result)
    

    def get_interest_rules_display(self) -> str:
        """Get formatted interest rules display"""
        result = ["Interest rules:"]
        result.append("| Date     | RuleId | Rate (%) |")
        
        for rule in self.interest_rules:
            result.append(str(rule))

        return "\n".join(result)
    
####################################### Example usage of class Banking System ####################################
bank = BankingSystem()

# print(bank.validate_date('291011232'))
# print(bank.validate_date('9101123'))
# print(bank.validate_date('20241018'))
# print(bank.validate_date('20240230'))


# print(bank.validate_amount(100.00))
# print(bank.validate_amount(100))
# print(bank.validate_amount(-67.22))
# print(bank.validate_amount(67.123))

# print(bank.define_interest_rule("20230101 RULE01 1.95"))
# bank.input_transaction("20230101 AC001 D 100.00")
# bank.input_transaction("20230115 AC001 W 50.00")
# bank.input_transaction("20230120 AC001 D 200.00")

# print(bank.get_account_statement("AC001"))
# print(bank.get_account_statement("AC999"))

# bank.define_interest_rule("20230101 RULE01 1.95")
# bank.define_interest_rule("20230520 RULE02 1.90")
# bank.define_interest_rule("20230615 RULE03 2.20")

# print(bank.get_interest_rules_display())
################################################ end ##################################################