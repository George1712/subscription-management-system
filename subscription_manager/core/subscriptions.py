from typing import List, Optional, Dict
from ..models import Subscription, Member, Plan
from ..database import execute_query, execute_insert
from ..utils.validators import validate_date
from ..utils.helpers import get_current_date, format_date, parse_date, add_days_to_date, get_confirmation
from ..utils.display import (display_success_message, display_error_message, display_warning_message)


class SubscriptionManager :
    def __init__(self) :
        pass

    def create_subscription(self, member_id: int, plan_id: int, 
                          start_date: str = None) -> Optional[Subscription] :

        # Check if member exists
        from .members import member_manager
        member = member_manager.get_member_by_id(member_id)
        if not member:
            display_error_message(f"Member with ID {member_id} not found")
            return None
            
        # Check if plan exists and is active
        from .plans import plan_manager
        plan = plan_manager.get_plan_by_id(plan_id)
        if not plan:
            display_error_message(f"Plan with ID {plan_id} not found")
            return None
        if not plan.is_active:
            display_error_message(f"Plan with ID {plan_id} is not active")
            return None
            
        # Validate and set start date
        if start_date:
            is_valid, error_msg = validate_date(start_date, "Start date")
            if not is_valid:
                display_error_message(error_msg)
                return None
        else:
            start_date = get_current_date()
            
        # Calculate end date
        end_date = add_days_to_date(start_date, plan.duration_days)
        
        try:
            active_subs = self.get_active_subscriptions_by_member(member_id)
            if active_subs :
                display_warning_message(f"Member already has an active subscription. This will replace it.")
                if not get_confirmation("Do you confirm replacing the current subscription ?") :
                    return None
        
            query = """
                INSERT INTO subscriptions (member_id, plan_id, start_date, end_date, is_active)
                VALUES (?, ?, ?, ?, ?)
            """
            subscription_id = execute_insert(query, (member_id, plan_id, start_date, end_date, True))
            
            if subscription_id:
                subscription = Subscription(
                    id=subscription_id,
                    member_id=member_id,
                    plan_id=plan_id,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True,
                    member=member,
                    plan=plan
                )
                display_success_message(f"Subscription created successfully with ID: {subscription_id}")
                return subscription
            else:
                display_error_message("Failed to create subscription")
                return None
                
        except Exception as e:
            display_error_message(f"Error creating subscription: {str(e)}")
            return None


    def _create_member_from_row(self, row):
        """Create a Member object from a database row"""
        return Member(
            id=row['member_id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            phone=row['phone']
        )
    def _create_plan_from_row(self, row):
        """Create a Plan object from a database row"""
        return Plan(
            id=row['plan_id'],
            name=row['plan_name'],
            duration_days=row['duration_days'],
            price=row['price']
        )
    def _create_subscription_from_row(self, row, member, plan):
        """Create a Subscription object from a database row with Member and Plan objects"""
        return Subscription(
            id=row['id'],
            member_id=row['member_id'],
            plan_id=row['plan_id'],
            start_date=row['start_date'],
            end_date=row['end_date'],
            is_active=bool(row['is_active']),
            member=member,
            plan=plan
        )
        


    def get_all_subscriptions(self, include_inactive: bool = False) -> List[Subscription]:

        try:
            if include_inactive:
                query = """
                    SELECT s.*, m.first_name, m.last_name, m.email, m.phone,
                           p.name as plan_name, p.duration_days, p.price
                    FROM subscriptions s
                    JOIN members m ON s.member_id = m.id
                    JOIN plans p ON s.plan_id = p.id
                    ORDER BY s.id
                """
            else:
                query = """
                    SELECT s.*, m.first_name, m.last_name, m.email, m.phone,
                           p.name as plan_name, p.duration_days, p.price
                    FROM subscriptions s
                    JOIN members m ON s.member_id = m.id
                    JOIN plans p ON s.plan_id = p.id
                    WHERE s.is_active = TRUE
                    ORDER BY s.id
                """
                
            rows = execute_query(query)
            
            subscriptions = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)
                subscriptions.append(subscription)
                
            return subscriptions
            
        except Exception as e:
            display_error_message(f"Error retrieving subscriptions: {str(e)}")
            return []


    def get_subscription_by_id(self, subscription_id: int) -> Optional[Subscription]:
        try:
            query = """
                SELECT s.*, m.first_name, m.last_name, m.email, m.phone,
                       p.name as plan_name, p.duration_days, p.price
                FROM subscriptions s
                JOIN members m ON s.member_id = m.id
                JOIN plans p ON s.plan_id = p.id
                WHERE s.id = ?
            """
            rows = execute_query(query, (subscription_id,))
            
            if rows:
                row = rows[0]
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)
                return subscription
            else:
                display_error_message(f"Subscription with ID {subscription_id} not found")
                return None
                
        except Exception as e:
            display_error_message(f"Error retrieving subscription: {str(e)}")
            return None


    def get_subscriptions_by_member(self, member_id: int) -> List[Subscription]:
        try:
            query = """
                SELECT s.*, m.first_name, m.last_name, m.email, m.phone, 
                       p.name as plan_name, p.duration_days, p.price
                FROM subscriptions s
                JOIN members m ON s.member_id = m.id
                JOIN plans p ON s.plan_id = p.id
                WHERE s.member_id = ?
                ORDER BY s.start_date DESC
            """
            rows = execute_query(query, (member_id,))
            
            subscriptions = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)
                subscriptions.append(subscription)
                
            return subscriptions
            
        except Exception as e:
            display_error_message(f"Error retrieving member subscriptions: {str(e)}")
            return []

    def get_active_subscriptions_by_member(self, member_id: int) -> List[Subscription]:
        try:
            query = """
                SELECT s.*, m.first_name, m.last_name, m.email, m.phone, 
                       p.name as plan_name, p.duration_days, p.price
                FROM subscriptions s
                JOIN members m ON s.member_id = m.id
                JOIN plans p ON s.plan_id = p.id
                WHERE s.member_id = ? AND s.is_active = TRUE
                ORDER BY s.start_date DESC
            """
            rows = execute_query(query, (member_id,))
            
            subscriptions = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)
                subscriptions.append(subscription)

            return subscriptions
            
        except Exception as e:
            display_error_message(f"Error retrieving active member subscriptions: {str(e)}")
            return []


    def renew_subscription(self, subscription_id:int) -> bool :
        subscription = self.get_subscription_by_id(subscription_id)
        if not subscription :
            return False
        
        current_end_date = parse_date(subscription.end_date)
        new_end_date = add_days_to_date(current_end_date, subscription.plan.duration_days)

        try :
            query = "UPDATE subscriptions SET end_date = ? WHERE id = ?"
            execute_query(query, (format_date(new_end_date), subscription_id))

            display_success_message(f"Subscription {subscription_id} renewed until {format_date(new_end_date)}")
            return True
        except Exception as e :
            display_error_message(f"Error renewing subscription: {str(e)}")
            return False

    def cancel_subscription(self, subscription_id: int) -> bool:
        try:
            query = "UPDATE subscriptions SET is_active = FALSE WHERE id = ?"
            execute_query(query, (subscription_id,))
            
            display_success_message(f"Subscription {subscription_id} cancelled successfully")
            return True
            
        except Exception as e:
            display_error_message(f"Error cancelling subscription: {str(e)}")
            return False

    def activate_subscription(self, subscription_id: int) -> bool:
        try:
            query = "UPDATE subscriptions SET is_active = TRUE WHERE id = ?"
            execute_query(query, (subscription_id,))
            
            display_success_message(f"Subscription {subscription_id} activated successfully")
            return True
            
        except Exception as e:
            display_error_message(f"Error activating subscription: {str(e)}")
            return False

    def get_expiring_subscriptions(self, days: int = 7) -> List[Subscription]:

        try:
            query = """
                SELECT s.*, m.first_name, m.last_name, m.email, m.phone, 
                       p.name as plan_name, p.duration_days, p.price
                FROM subscriptions s
                JOIN members m ON s.member_id = m.id
                JOIN plans p ON s.plan_id = p.id
                WHERE s.is_active = TRUE 
                AND s.end_date BETWEEN date('now') AND date('now', ?)
                ORDER BY s.end_date ASC
            """
            rows = execute_query(query, (f"+{days} days",))
            
            subscriptions = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)
                subscriptions.append(subscription)
                
            return subscriptions
            
        except Exception as e:
            display_error_message(f"Error retrieving expiring subscriptions: {str(e)}")
            return []

    def get_expired_subscriptions(self) -> List[Subscription]:

        try:
            query = """
                SELECT s.*, m.first_name, m.last_name, m.email, m.phone, 
                       p.name as plan_name, p.duration_days, p.price
                FROM subscriptions s
                JOIN members m ON s.member_id = m.id
                JOIN plans p ON s.plan_id = p.id
                WHERE s.is_active = TRUE 
                AND s.end_date < date('now')
                ORDER BY s.end_date ASC
            """
            rows = execute_query(query)
            
            subscriptions = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)
                subscriptions.append(subscription)

            return subscriptions
            
        except Exception as e:
            display_error_message(f"Error retrieving expired subscriptions: {str(e)}")
            return []

    def get_subscription_stats(self) -> Dict[str, int]:
        try:
            query_total = "SELECT COUNT(*) as count FROM subscriptions"
            query_active = "SELECT COUNT(*) as count FROM subscriptions WHERE is_active = TRUE"
            query_expired = "SELECT COUNT(*) as count FROM subscriptions WHERE is_active = TRUE AND end_date < date('now')"
            query_expiring = """
                SELECT COUNT(*) as count FROM subscriptions 
                WHERE is_active = TRUE 
                AND end_date BETWEEN date('now') AND date('now', '+7 days')
            """
            
            total = execute_query(query_total)[0]['count']
            active = execute_query(query_active)[0]['count']
            expired = execute_query(query_expired)[0]['count']
            expiring = execute_query(query_expiring)[0]['count']
            
            return {
                'total_subscriptions': total,
                'active_subscriptions': active,
                'expired_subscriptions': expired,
                'expiring_subscriptions': expiring
            }
            
        except Exception as e:
            display_error_message(f"Error retrieving subscription statistics: {str(e)}")
            return {
                'total_subscriptions': 0,
                'active_subscriptions': 0,
                'expired_subscriptions': 0,
                'expiring_subscriptions': 0
            }

# Singleton instance for use throughout the application
subscription_manager = SubscriptionManager()

# Import managers at the end to avoid circular imports
