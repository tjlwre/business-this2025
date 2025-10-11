"""
Course service for BusinessThis
Handles educational content, course management, and learning progress
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import json

class CourseService:
    """Course service for educational content and learning management"""
    
    def __init__(self):
        self.courses = {
            'budgeting_basics': {
                'id': 'budgeting_basics',
                'title': 'Budgeting Basics: Take Control of Your Money',
                'description': 'Learn the fundamentals of budgeting and money management',
                'price': 49.99,
                'duration_hours': 3,
                'difficulty': 'beginner',
                'instructor': 'Sarah Johnson, CFP',
                'modules': [
                    {
                        'id': 'module_1',
                        'title': 'Understanding Your Income and Expenses',
                        'duration_minutes': 30,
                        'content_type': 'video',
                        'description': 'Learn how to track and categorize your income and expenses'
                    },
                    {
                        'id': 'module_2',
                        'title': 'Creating Your First Budget',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Step-by-step guide to creating a realistic budget'
                    },
                    {
                        'id': 'module_3',
                        'title': 'Budgeting Tools and Apps',
                        'duration_minutes': 30,
                        'content_type': 'video',
                        'description': 'Explore different budgeting methods and tools'
                    },
                    {
                        'id': 'module_4',
                        'title': 'Sticking to Your Budget',
                        'duration_minutes': 30,
                        'content_type': 'video',
                        'description': 'Strategies for maintaining your budget long-term'
                    }
                ],
                'learning_objectives': [
                    'Understand the importance of budgeting',
                    'Create a realistic monthly budget',
                    'Use budgeting tools effectively',
                    'Maintain budget discipline'
                ],
                'prerequisites': 'None',
                'certificate': True
            },
            'debt_elimination': {
                'id': 'debt_elimination',
                'title': 'Debt Elimination Strategies',
                'description': 'Master proven methods to eliminate debt and build wealth',
                'price': 79.99,
                'duration_hours': 5,
                'difficulty': 'intermediate',
                'instructor': 'Michael Chen, CPA',
                'modules': [
                    {
                        'id': 'module_1',
                        'title': 'Understanding Different Types of Debt',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Learn about credit cards, loans, and other debt types'
                    },
                    {
                        'id': 'module_2',
                        'title': 'Debt Avalanche vs Debt Snowball',
                        'duration_minutes': 60,
                        'content_type': 'video',
                        'description': 'Compare different debt payoff strategies'
                    },
                    {
                        'id': 'module_3',
                        'title': 'Negotiating with Creditors',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'How to negotiate better terms with creditors'
                    },
                    {
                        'id': 'module_4',
                        'title': 'Building an Emergency Fund',
                        'duration_minutes': 30,
                        'content_type': 'video',
                        'description': 'Why emergency funds are crucial for debt elimination'
                    },
                    {
                        'id': 'module_5',
                        'title': 'Preventing Future Debt',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Strategies to avoid accumulating new debt'
                    }
                ],
                'learning_objectives': [
                    'Identify different debt elimination strategies',
                    'Negotiate with creditors effectively',
                    'Build an emergency fund',
                    'Prevent future debt accumulation'
                ],
                'prerequisites': 'Basic understanding of personal finance',
                'certificate': True
            },
            'investment_fundamentals': {
                'id': 'investment_fundamentals',
                'title': 'Investment Fundamentals for Beginners',
                'description': 'Learn how to start investing and build long-term wealth',
                'price': 99.99,
                'duration_hours': 6,
                'difficulty': 'intermediate',
                'instructor': 'David Rodriguez, CFA',
                'modules': [
                    {
                        'id': 'module_1',
                        'title': 'Introduction to Investing',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Understanding the basics of investing and market principles'
                    },
                    {
                        'id': 'module_2',
                        'title': 'Asset Classes and Diversification',
                        'duration_minutes': 60,
                        'content_type': 'video',
                        'description': 'Learn about stocks, bonds, and other investment vehicles'
                    },
                    {
                        'id': 'module_3',
                        'title': 'Risk vs Return',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Understanding risk tolerance and expected returns'
                    },
                    {
                        'id': 'module_4',
                        'title': 'Building Your First Portfolio',
                        'duration_minutes': 60,
                        'content_type': 'video',
                        'description': 'Step-by-step portfolio construction for beginners'
                    },
                    {
                        'id': 'module_5',
                        'title': 'Tax-Advantaged Accounts',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Understanding 401(k), IRA, and other tax-advantaged accounts'
                    },
                    {
                        'id': 'module_6',
                        'title': 'Common Investment Mistakes',
                        'duration_minutes': 30,
                        'content_type': 'video',
                        'description': 'Avoiding common pitfalls in investing'
                    }
                ],
                'learning_objectives': [
                    'Understand basic investment principles',
                    'Build a diversified portfolio',
                    'Choose appropriate investment accounts',
                    'Avoid common investment mistakes'
                ],
                'prerequisites': 'Basic understanding of personal finance',
                'certificate': True
            },
            'retirement_planning': {
                'id': 'retirement_planning',
                'title': 'Comprehensive Retirement Planning',
                'description': 'Plan for a secure and comfortable retirement',
                'price': 149.99,
                'duration_hours': 8,
                'difficulty': 'advanced',
                'instructor': 'Jennifer Lee, CFP',
                'modules': [
                    {
                        'id': 'module_1',
                        'title': 'Retirement Planning Basics',
                        'duration_minutes': 60,
                        'content_type': 'video',
                        'description': 'Understanding retirement planning fundamentals'
                    },
                    {
                        'id': 'module_2',
                        'title': 'Social Security Optimization',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Maximizing your Social Security benefits'
                    },
                    {
                        'id': 'module_3',
                        'title': '401(k) and IRA Strategies',
                        'duration_minutes': 60,
                        'content_type': 'video',
                        'description': 'Advanced strategies for retirement accounts'
                    },
                    {
                        'id': 'module_4',
                        'title': 'Healthcare in Retirement',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Planning for healthcare costs in retirement'
                    },
                    {
                        'id': 'module_5',
                        'title': 'Estate Planning Basics',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Protecting your assets and loved ones'
                    },
                    {
                        'id': 'module_6',
                        'title': 'Creating Your Retirement Plan',
                        'duration_minutes': 60,
                        'content_type': 'workshop',
                        'description': 'Hands-on workshop to create your retirement plan'
                    }
                ],
                'learning_objectives': [
                    'Create a comprehensive retirement plan',
                    'Optimize Social Security benefits',
                    'Maximize retirement account contributions',
                    'Plan for healthcare and estate needs'
                ],
                'prerequisites': 'Intermediate understanding of personal finance',
                'certificate': True
            },
            'tax_optimization': {
                'id': 'tax_optimization',
                'title': 'Tax Optimization Strategies',
                'description': 'Minimize your tax burden and maximize your savings',
                'price': 129.99,
                'duration_hours': 4,
                'difficulty': 'advanced',
                'instructor': 'Robert Kim, CPA',
                'modules': [
                    {
                        'id': 'module_1',
                        'title': 'Understanding Tax Brackets',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'How tax brackets work and how to optimize them'
                    },
                    {
                        'id': 'module_2',
                        'title': 'Tax-Advantaged Investment Accounts',
                        'duration_minutes': 60,
                        'content_type': 'video',
                        'description': 'Maximizing 401(k), IRA, and HSA contributions'
                    },
                    {
                        'id': 'module_3',
                        'title': 'Deductions and Credits',
                        'duration_minutes': 45,
                        'content_type': 'video',
                        'description': 'Identifying and maximizing deductions and credits'
                    },
                    {
                        'id': 'module_4',
                        'title': 'Tax-Loss Harvesting',
                        'duration_minutes': 30,
                        'content_type': 'video',
                        'description': 'Advanced strategy for reducing tax liability'
                    }
                ],
                'learning_objectives': [
                    'Understand tax optimization strategies',
                    'Maximize tax-advantaged accounts',
                    'Identify deductions and credits',
                    'Implement tax-loss harvesting'
                ],
                'prerequisites': 'Intermediate understanding of personal finance',
                'certificate': True
            }
        }
    
    def get_course_catalog(self, category: str = 'all', difficulty: str = 'all') -> Dict[str, Any]:
        """Get course catalog with filtering options"""
        try:
            courses = list(self.courses.values())
            
            # Filter by category (if implemented)
            if category != 'all':
                # In a real implementation, courses would have categories
                pass
            
            # Filter by difficulty
            if difficulty != 'all':
                courses = [course for course in courses if course['difficulty'] == difficulty]
            
            # Sort by price
            courses.sort(key=lambda x: x['price'])
            
            return {
                'courses': courses,
                'total_count': len(courses),
                'categories': ['all', 'budgeting', 'debt', 'investment', 'retirement', 'tax'],
                'difficulties': ['all', 'beginner', 'intermediate', 'advanced']
            }
            
        except Exception as e:
            return {'error': f'Error getting course catalog: {str(e)}'}
    
    def get_course_details(self, course_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific course"""
        try:
            course = self.courses.get(course_id)
            if not course:
                return {'error': 'Course not found'}
            
            return {
                'course': course,
                'instructor_bio': self._get_instructor_bio(course['instructor']),
                'reviews': self._get_course_reviews(course_id),
                'related_courses': self._get_related_courses(course_id)
            }
            
        except Exception as e:
            return {'error': f'Error getting course details: {str(e)}'}
    
    def enroll_user_in_course(self, user_id: str, course_id: str, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enroll user in a course"""
        try:
            course = self.courses.get(course_id)
            if not course:
                return {'error': 'Course not found'}
            
            # In a real implementation, this would:
            # 1. Process payment
            # 2. Create enrollment record
            # 3. Send confirmation email
            
            enrollment = {
                'user_id': user_id,
                'course_id': course_id,
                'enrollment_date': datetime.utcnow().isoformat(),
                'status': 'enrolled',
                'progress': 0,
                'completed_modules': [],
                'certificate_earned': False
            }
            
            return {
                'success': True,
                'enrollment': enrollment,
                'message': f'Successfully enrolled in {course["title"]}'
            }
            
        except Exception as e:
            return {'error': f'Error enrolling in course: {str(e)}'}
    
    def get_user_courses(self, user_id: str) -> Dict[str, Any]:
        """Get user's enrolled courses and progress"""
        try:
            # In a real implementation, this would query the database
            user_courses = {
                'enrolled_courses': [],
                'completed_courses': [],
                'certificates': [],
                'total_progress': 0
            }
            
            return user_courses
            
        except Exception as e:
            return {'error': f'Error getting user courses: {str(e)}'}
    
    def update_course_progress(self, user_id: str, course_id: str, module_id: str) -> Dict[str, Any]:
        """Update user's progress in a course"""
        try:
            # In a real implementation, this would:
            # 1. Update progress in database
            # 2. Check if course is completed
            # 3. Issue certificate if applicable
            
            progress_update = {
                'user_id': user_id,
                'course_id': course_id,
                'module_id': module_id,
                'completed_at': datetime.utcnow().isoformat(),
                'progress_percentage': 0  # Calculate based on completed modules
            }
            
            return {
                'success': True,
                'progress': progress_update,
                'message': 'Progress updated successfully'
            }
            
        except Exception as e:
            return {'error': f'Error updating course progress: {str(e)}'}
    
    def get_course_certificate(self, user_id: str, course_id: str) -> Dict[str, Any]:
        """Get course certificate for completed course"""
        try:
            # In a real implementation, this would:
            # 1. Check if course is completed
            # 2. Generate certificate
            # 3. Return certificate data
            
            certificate = {
                'user_id': user_id,
                'course_id': course_id,
                'certificate_id': f"cert_{user_id}_{course_id}_{int(datetime.utcnow().timestamp())}",
                'issued_date': datetime.utcnow().isoformat(),
                'course_title': self.courses.get(course_id, {}).get('title', ''),
                'instructor': self.courses.get(course_id, {}).get('instructor', ''),
                'certificate_url': f"https://businessthis.com/certificates/{user_id}/{course_id}"
            }
            
            return {
                'success': True,
                'certificate': certificate
            }
            
        except Exception as e:
            return {'error': f'Error getting course certificate: {str(e)}'}
    
    def get_learning_recommendations(self, user_id: str, user_profile: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get personalized course recommendations"""
        try:
            recommendations = []
            
            # Analyze user profile for recommendations
            if user_profile:
                # Budgeting recommendation
                if user_profile.get('monthly_savings', 0) < 0:
                    recommendations.append({
                        'course_id': 'budgeting_basics',
                        'reason': 'Your expenses exceed your income. Learn budgeting basics to get back on track.',
                        'priority': 'high'
                    })
                
                # Debt elimination recommendation
                if user_profile.get('total_debt', 0) > 0:
                    recommendations.append({
                        'course_id': 'debt_elimination',
                        'reason': 'You have outstanding debt. Learn proven strategies to eliminate it.',
                        'priority': 'high'
                    })
                
                # Investment recommendation
                if user_profile.get('monthly_savings', 0) > 500:
                    recommendations.append({
                        'course_id': 'investment_fundamentals',
                        'reason': 'You have good savings. Learn how to invest and grow your wealth.',
                        'priority': 'medium'
                    })
                
                # Retirement planning recommendation
                if user_profile.get('age', 0) >= 30:
                    recommendations.append({
                        'course_id': 'retirement_planning',
                        'reason': 'It\'s never too early to plan for retirement. Start building your future.',
                        'priority': 'medium'
                    })
            
            # Default recommendations if no profile
            if not recommendations:
                recommendations = [
                    {
                        'course_id': 'budgeting_basics',
                        'reason': 'Start with the fundamentals of personal finance.',
                        'priority': 'high'
                    },
                    {
                        'course_id': 'investment_fundamentals',
                        'reason': 'Learn how to grow your money through investing.',
                        'priority': 'medium'
                    }
                ]
            
            return {
                'recommendations': recommendations,
                'total_count': len(recommendations)
            }
            
        except Exception as e:
            return {'error': f'Error getting learning recommendations: {str(e)}'}
    
    def _get_instructor_bio(self, instructor_name: str) -> str:
        """Get instructor biography"""
        bios = {
            'Sarah Johnson, CFP': 'Certified Financial Planner with 10+ years of experience helping individuals achieve their financial goals.',
            'Michael Chen, CPA': 'Certified Public Accountant specializing in debt management and financial recovery strategies.',
            'David Rodriguez, CFA': 'Chartered Financial Analyst with expertise in investment management and portfolio construction.',
            'Jennifer Lee, CFP': 'Certified Financial Planner focusing on retirement planning and wealth preservation.',
            'Robert Kim, CPA': 'Certified Public Accountant with extensive experience in tax planning and optimization strategies.'
        }
        
        return bios.get(instructor_name, 'Experienced financial professional with expertise in personal finance.')
    
    def _get_course_reviews(self, course_id: str) -> List[Dict[str, Any]]:
        """Get course reviews and ratings"""
        # In a real implementation, this would query the database
        return [
            {
                'user_name': 'John D.',
                'rating': 5,
                'review': 'Excellent course! Very practical and easy to follow.',
                'date': '2024-01-15'
            },
            {
                'user_name': 'Sarah M.',
                'rating': 4,
                'review': 'Great content, helped me understand the basics.',
                'date': '2024-01-10'
            }
        ]
    
    def _get_related_courses(self, course_id: str) -> List[Dict[str, Any]]:
        """Get related courses based on current course"""
        # In a real implementation, this would use recommendation algorithms
        related_courses = []
        
        for course in self.courses.values():
            if course['id'] != course_id:
                related_courses.append({
                    'id': course['id'],
                    'title': course['title'],
                    'price': course['price'],
                    'difficulty': course['difficulty']
                })
        
        return related_courses[:3]  # Return top 3 related courses
