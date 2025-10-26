"""
Savings Goal model for BusinessThis
"""
from datetime import datetime, date
from typing import Optional, Dict, Any
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class SavingsGoal:
    """Savings Goal model"""
    id: str
    user_id: str
    name: str
    target_amount: Decimal
    current_amount: Decimal = Decimal('0')
    target_date: Optional[date] = None
    monthly_contribution: Optional[Decimal] = None
    priority: int = 1
    is_achieved: bool = False
    achieved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert savings goal to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'target_amount': float(self.target_amount),
            'current_amount': float(self.current_amount),
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'monthly_contribution': float(self.monthly_contribution) if self.monthly_contribution else None,
            'priority': self.priority,
            'is_achieved': self.is_achieved,
            'achieved_at': self.achieved_at.isoformat() if self.achieved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SavingsGoal':
        """Create savings goal from dictionary"""
        return cls(
            id=data['id'],
            user_id=data['user_id'],
            name=data['name'],
            target_amount=Decimal(str(data['target_amount'])),
            current_amount=Decimal(str(data.get('current_amount', 0))),
            target_date=date.fromisoformat(data['target_date']) if data.get('target_date') else None,
            monthly_contribution=Decimal(str(data['monthly_contribution'])) if data.get('monthly_contribution') else None,
            priority=data.get('priority', 1),
            is_achieved=data.get('is_achieved', False),
            achieved_at=datetime.fromisoformat(data['achieved_at']) if data.get('achieved_at') else None,
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    def calculate_progress_percentage(self) -> float:
        """Calculate progress as percentage"""
        if self.target_amount == 0:
            return 0.0
        return float((self.current_amount / self.target_amount) * 100)
    
    def calculate_remaining_amount(self) -> Decimal:
        """Calculate remaining amount to reach goal"""
        return max(Decimal('0'), self.target_amount - self.current_amount)
    
    def calculate_months_to_goal(self) -> Optional[int]:
        """Calculate months needed to reach goal based on monthly contribution"""
        if not self.monthly_contribution or self.monthly_contribution <= 0:
            return None
        
        remaining = self.calculate_remaining_amount()
        if remaining <= 0:
            return 0
        
        months = remaining / self.monthly_contribution
        return int(months) + (1 if months % 1 > 0 else 0)
    
    def calculate_required_monthly_contribution(self, months: int) -> Decimal:
        """Calculate required monthly contribution to reach goal in given months"""
        if months <= 0:
            return Decimal('0')
        
        remaining = self.calculate_remaining_amount()
        return remaining / months
    
    def is_on_track(self) -> bool:
        """Check if goal is on track based on target date and monthly contribution"""
        if not self.target_date or not self.monthly_contribution:
            return True  # Can't determine if on track
        
        months_needed = self.calculate_months_to_goal()
        if months_needed is None:
            return True
        
        # Calculate months until target date
        today = date.today()
        months_until_target = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)
        
        return months_needed <= months_until_target
    
    def should_be_achieved(self) -> bool:
        """Check if goal should be marked as achieved"""
        return self.current_amount >= self.target_amount and not self.is_achieved
