"""
Financial Profile model for BusinessThis
"""
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class FinancialProfile:
    """Financial Profile model"""
    id: str
    user_id: str
    monthly_income: Decimal = Decimal('0')
    fixed_expenses: Decimal = Decimal('0')
    variable_expenses: Decimal = Decimal('0')
    emergency_fund_target: Decimal = Decimal('0')
    emergency_fund_current: Decimal = Decimal('0')
    total_debt: Decimal = Decimal('0')
    credit_score: Optional[int] = None
    risk_tolerance: str = 'moderate'
    age: Optional[int] = None
    retirement_age: int = 65
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert financial profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'monthly_income': float(self.monthly_income),
            'fixed_expenses': float(self.fixed_expenses),
            'variable_expenses': float(self.variable_expenses),
            'emergency_fund_target': float(self.emergency_fund_target),
            'emergency_fund_current': float(self.emergency_fund_current),
            'total_debt': float(self.total_debt),
            'credit_score': self.credit_score,
            'risk_tolerance': self.risk_tolerance,
            'age': self.age,
            'retirement_age': self.retirement_age,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FinancialProfile':
        """Create financial profile from dictionary"""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            monthly_income=Decimal(str(data.get('monthly_income', 0))),
            fixed_expenses=Decimal(str(data.get('fixed_expenses', 0))),
            variable_expenses=Decimal(str(data.get('variable_expenses', 0))),
            emergency_fund_target=Decimal(str(data.get('emergency_fund_target', 0))),
            emergency_fund_current=Decimal(str(data.get('emergency_fund_current', 0))),
            total_debt=Decimal(str(data.get('total_debt', 0))),
            credit_score=data.get('credit_score'),
            risk_tolerance=data.get('risk_tolerance', 'moderate'),
            age=data.get('age'),
            retirement_age=data.get('retirement_age', 65),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    def calculate_debt_to_income_ratio(self) -> float:
        """Calculate debt-to-income ratio"""
        if self.monthly_income == 0:
            return 0.0
        return float(self.total_debt / self.monthly_income)
    
    def calculate_savings_rate(self) -> float:
        """Calculate savings rate as percentage"""
        if self.monthly_income == 0:
            return 0.0
        total_expenses = self.fixed_expenses + self.variable_expenses
        savings = self.monthly_income - total_expenses
        return float((savings / self.monthly_income) * 100)
    
    def calculate_emergency_fund_progress(self) -> float:
        """Calculate emergency fund progress as percentage"""
        if self.emergency_fund_target == 0:
            return 0.0
        return float((self.emergency_fund_current / self.emergency_fund_target) * 100)
    
    def get_recommended_emergency_fund(self) -> Decimal:
        """Get recommended emergency fund amount (3-6 months expenses)"""
        total_monthly_expenses = self.fixed_expenses + self.variable_expenses
        return total_monthly_expenses * 6  # 6 months recommended
    
    def is_emergency_fund_adequate(self) -> bool:
        """Check if emergency fund is adequate (6 months expenses)"""
        recommended = self.get_recommended_emergency_fund()
        return self.emergency_fund_current >= recommended
