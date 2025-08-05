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
    pass

class TestAccount(unittest.TestCase):
    """Test Account class"""
    pass

class TestBankingSystem(unittest.TestCase):
    """Test BankingSystem class"""
    pass

class TestIntegration(unittest.TestCase):
    """Integration Tests"""
    pass

if __name__=='__main__':
    unittest.main(verbosity=2)