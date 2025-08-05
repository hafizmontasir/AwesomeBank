"""Unit tests for the AwesomeGIC Banking System"""

import unittest
from decimal import Decimal
from bank_system import BankingSystem, Account, Transaction, InterestRule

class TestTransaction(unittest.TestCase):
    """Test Transaction class"""
    
    def test_transaction_creation(self):
        """Test transaction object creation"""
        txn = Transaction("20230626", "AC001", "D", Decimal('100.00'), "20230626-01")
        self.assertEqual(txn.date, "20230626")
        self.assertEqual(txn.account, "AC001")
        self.assertEqual(txn.txn_type, "D")
        self.assertEqual(txn.amount, Decimal("100.00"))
        self.assertEqual(txn.id, "20230626-01")
    
    def test_transaction_type_case_insensitive(self):
        """Test Transaction type is converted to uppercase"""
        txn = Transaction("20230626", "AC001", "d", Decimal('100.00'), "20230626-01")
        self.assertEqual(txn.txn_type, "D")
        
        txn2 = Transaction("20230626", "AC001", "w", Decimal('100.00'), "20230626-01")
        self.assertEqual(txn2.txn_type, "W")
    
class TestInterestRule(unittest.TestCase):
    """Test InterestRule class"""
    
    def test_interest_rule_creation(self):
        rule = InterestRule("20230615", "RULE03", Decimal('2.20'))
        self.assertEqual(rule.date, "20230615")
        self.assertEqual(rule.rule_id, "RULE03")
        self.assertEqual(rule.rate, Decimal('2.20'))

class TestAccount(unittest.TestCase):
    """Test Account class"""
    def setUp(self):
        """setup test account"""
        self.account = Account("AC001")

    def test_account_creation(self):
        """Test account object creation"""
        self.assertEqual(self.account.account_id, "AC001")
        self.assertEqual(len(self.account.transactions), 0)
        self.assertEqual(self.account.balance, Decimal('0'))
        
    def test_withdrawal_transaction(self):
        """Test adding withdrawl transaction"""
        deposit = Transaction("20230626", "AC001", "D", Decimal('100.00'))
        self.account.add_transaction(deposit)
        
        withdrawal = Transaction("20230627", "AC001", "W", Decimal('50.00'))
        self.account.add_transaction(withdrawal)
        
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.balance, Decimal('50.00'))
        
    def test_insufficient_balance_withdrawal(self):
        """Test withdrawal with insufficient balance"""
        withdrawal = Transaction("20230626", "AC001", "W", Decimal('100.00'))

        with self.assertRaise(ValueError):
            self.account.add_transaction(withdrawal)

    def test_interest_transaction(self):
        """Test adding interest transaction"""
        deposit = Transaction("20230626", "AC001", "D", Decimal('100.00'))
        self.account.add_transaction(deposit)
        
        interest = Transaction("20230630", "AC001", "I", Decimal('0.39'))
        self.account.add_transaction(interest)
        
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.balance, Decimal('100.39'))
        
    def test_get_balance_at_date(self):
        """Test getting balance at specific date"""

        txn1 = Transaction("20230601", "AC001", "D", Decimal('100.00'))
        txn2 = Transaction("20230615", "AC001", "D", Decimal('50.00'))
        txn3 = Transaction("20230620", "AC001", "W", Decimal('30.00'))

        self.account.add_transaction(txn1)
        self.account.add_transaction(txn2)
        self.account.add_transaction(txn3)

        self.assertEqual(self.account.get_balance_at_date('20230531'), Decimal('0'))
        self.assertEqual(self.account.get_balance_at_date('20230601'), Decimal('100.00'))
        self.assertEqual(self.account.get_balance_at_date('20230615'), Decimal('150.00'))
        self.assertEqual(self.account.get_balance_at_date('20230620'), Decimal('120.00'))




class TestBankingSystem(unittest.TestCase):
    """Test BankingSystem class"""
    pass

class TestIntegration(unittest.TestCase):
    """Integration Tests"""
    pass

if __name__=='__main__':
    unittest.main(verbosity=2)