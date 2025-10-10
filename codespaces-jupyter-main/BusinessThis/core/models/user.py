"""
User model for BusinessThis
"""
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class User:
    """User model"""
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    subscription_tier: str = 'free'
    subscription_status: str = 'active'
    subscription_expires_at: Optional[datetime] = None
    ai_usage_count: int = 0
    ai_usage_limit: int = 0
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'subscription_tier': self.subscription_tier,
            'subscription_status': self.subscription_status,
            'subscription_expires_at': self.subscription_expires_at.isoformat() if self.subscription_expires_at else None,
            'ai_usage_count': self.ai_usage_count,
            'ai_usage_limit': self.ai_usage_limit,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create user from dictionary"""
        return cls(
            id=data['id'],
            email=data['email'],
            full_name=data.get('full_name'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            subscription_tier=data.get('subscription_tier', 'free'),
            subscription_status=data.get('subscription_status', 'active'),
            subscription_expires_at=datetime.fromisoformat(data['subscription_expires_at']) if data.get('subscription_expires_at') else None,
            ai_usage_count=data.get('ai_usage_count', 0),
            ai_usage_limit=data.get('ai_usage_limit', 0),
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            is_active=data.get('is_active', True)
        )
    
    def is_premium(self) -> bool:
        """Check if user has premium subscription"""
        return self.subscription_tier in ['premium', 'pro']
    
    def is_pro(self) -> bool:
        """Check if user has pro subscription"""
        return self.subscription_tier == 'pro'
    
    def can_use_ai(self) -> bool:
        """Check if user can use AI features"""
        if self.subscription_tier == 'free':
            return False
        elif self.subscription_tier == 'premium':
            return self.ai_usage_count < 50  # 50 AI calls per month for premium
        else:  # pro
            return True  # Unlimited for pro users
    
    def get_ai_usage_limit(self) -> int:
        """Get AI usage limit based on subscription tier"""
        if self.subscription_tier == 'free':
            return 0
        elif self.subscription_tier == 'premium':
            return 50
        else:  # pro
            return -1  # Unlimited
