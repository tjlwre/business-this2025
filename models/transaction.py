"""
Transaction model for BusinessThis
"""
from datetime import datetime, date
from typing import Optional, Dict, Any
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Transaction:
    """Transaction model"""
    id: str
    user_id: str
    amount: Decimal
    description: Optional[str] = None
    category: Optional[str] = None
    transaction_type: str = 'expense'  # 'income', 'expense', 'transfer'
    date: date = None
    account_name: Optional[str] = None
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'description': self.description,
            'category': self.category,
            'transaction_type': self.transaction_type,
            'date': self.date.isoformat() if self.date else None,
            'account_name': self.account_name,
            'is_recurring': self.is_recurring,
            'recurring_frequency': self.recurring_frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create transaction from dictionary"""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            amount=Decimal(str(data['amount'])),
            description=data.get('description'),
            category=data.get('category'),
            transaction_type=data.get('transaction_type', 'expense'),
            date=date.fromisoformat(data['date']) if data.get('date') else None,
            account_name=data.get('account_name'),
            is_recurring=data.get('is_recurring', False),
            recurring_frequency=data.get('recurring_frequency'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    def is_income(self) -> bool:
        """Check if transaction is income"""
        return self.transaction_type == 'income'
    
    def is_expense(self) -> bool:
        """Check if transaction is expense"""
        return self.transaction_type == 'expense'
    
    def is_transfer(self) -> bool:
        """Check if transaction is transfer"""
        return self.transaction_type == 'transfer'
    
    def get_absolute_amount(self) -> Decimal:
        """Get absolute amount (positive for income, negative for expense)"""
        if self.is_income():
            return abs(self.amount)
        else:
            return -abs(self.amount)
    
    def get_category_display_name(self) -> str:
        """Get display name for category"""
        if not self.category:
            return 'Uncategorized'
        
        category_map = {
            'food': 'Food & Dining',
            'transportation': 'Transportation',
            'housing': 'Housing',
            'utilities': 'Utilities',
            'entertainment': 'Entertainment',
            'healthcare': 'Healthcare',
            'shopping': 'Shopping',
            'education': 'Education',
            'travel': 'Travel',
            'insurance': 'Insurance',
            'savings': 'Savings',
            'investment': 'Investment',
            'salary': 'Salary',
            'freelance': 'Freelance',
            'investment_income': 'Investment Income',
            'other': 'Other'
        }
        
        return category_map.get(self.category.lower(), self.category.title())
