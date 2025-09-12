from typing import List, Optional, Dict, Any
from datetime import date, datetime
from ..models import Payment, Subscription, Member, Plan
from ..database import execute_query, execute_insert
from ..utils.validators import validate_date, validate_positive_number, validate_date_ranges, validate_payment_date_range
from ..utils.helpers import get_current_date, format_date, parse_date, format_currency, sanitize_input
from ..utils.display import (display_payments_table, display_success_message, 
                          display_error_message, display_info_message)

class PaymentManager:
    def __init__(self):
        pass
    # Helper Functions
    def _create_member_from_row(self, row):
        row = dict(row)
        return Member(
            id=row['member_id'] if 'member_id' in row else None,
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            phone=row.get('phone'),  # Use get() for optional fields
            date_joined=row.get('date_joined'),
            status=row.get('status')
        )
    def _create_plan_from_row(self, row):
        row = dict(row)
        return Plan(
            id=row['plan_id'] if 'plan_id' in row else None,
            name=row['plan_name'],
            description=row.get('description'),
            duration_days=row['duration_days'],
            price=row['price'],
            is_active=bool(row.get('is_active', True))
        )
    def _create_subscription_from_row(self, row, member, plan):
        return Subscription(
            id=row['subscription_id'],
            member_id=row['member_id'] if 'member_id' in row else None,
            plan_id=row['plan_id'] if 'plan_id' in row else None,
            start_date=row['start_date'],
            end_date=row['end_date'],
            is_active=bool(row['is_active']),
            member=member,
            plan=plan
        )
    def _create_payment_from_row(self, row, subscription=None):
        return Payment(
            id=row['id'],
            subscription_id=row['subscription_id'],
            amount=row['amount'],
            payment_date=row['payment_date'],
            notes=row['notes'],
            subscription=subscription
        )


    def record_payment(self, subscription_id: int, amount: float, 
                      payment_date: str = None, notes: str = None) -> Optional[Payment]:
        # Check if subscription exists
        from .subscriptions import subscription_manager
        subscription = subscription_manager.get_subscription_by_id(subscription_id)
        if not subscription:
            display_error_message(f"Subscription with ID {subscription_id} not found")
            return None
            
        # Validate amount
        is_valid, error_msg = validate_positive_number(amount, "Amount", allow_zero=False)
        if not is_valid:
            display_error_message(error_msg)
            return None
            
        # Validate and set payment date
        if payment_date:
            is_valid, error_msg = validate_date(payment_date, "Payment date")
            if not is_valid:
                display_error_message(error_msg)
                return None
        else:
            payment_date = get_current_date()
            
        notes = sanitize_input(notes)
            
        try:
            query = """
                INSERT INTO payments (subscription_id, amount, payment_date, notes)
                VALUES (?, ?, ?, ?)
            """
            payment_id = execute_insert(query, (subscription_id, amount, payment_date, notes))
            
            if payment_id:
                payment = Payment(
                    id = payment_id,
                    subscription_id = subscription_id,
                    amount = amount,
                    payment_date = payment_date,
                    notes = notes,
                    subscription = subscription
                )
                display_success_message(f"Payment recorded successfully with ID: {payment_id}")
                return payment
            else:
                display_error_message("Failed to record payment")
                return None
                
        except Exception as e:
            display_error_message(f"Error recording payment: {str(e)}")
            return None



    def get_all_payments(self) -> List[Payment]:
        try:
            query = """
                SELECT p.*, 
                s.member_id, s.plan_id, s.start_date, s.end_date, s.is_active,
                m.first_name, m.last_name, m.email, m.phone, m.date_joined, m.status,
                pl.name as plan_name, pl.description, pl.duration_days, pl.price, pl.is_active as plan_is_active
                FROM payments p
                JOIN subscriptions s ON p.subscription_id = s.id
                JOIN members m ON s.member_id = m.id
                JOIN plans pl ON s.plan_id = pl.id
                ORDER BY p.payment_date DESC, p.id DESC
            """
            rows = execute_query(query)
            
            payments = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)                
                payment = self._create_payment_from_row(row, subscription)
                payments.append(payment)
                
            return payments
            
        except Exception as e:
            display_error_message(f"Error retrieving payments: {str(e)}")
            return []

    def get_payment_by_id(self, payment_id:int) -> Optional[Payment]:
        try:
            query = """
                SELECT p.*, 
                s.member_id, s.plan_id, s.start_date, s.end_date, s.is_active,
                m.first_name, m.last_name, m.email, m.phone, m.date_joined, m.status,
                pl.name as plan_name, pl.description, pl.duration_days, pl.price, pl.is_active as plan_is_active
                FROM payments p
                JOIN subscriptions s ON p.subscription_id = s.id
                JOIN members m ON s.member_id = m.id
                JOIN plans pl ON s.plan_id = pl.id
                WHERE p.id = ?
            """
            rows = execute_query(query, (payment_id,))
            
            if rows:
                row = rows[0]
                
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)                
                return self._create_payment_from_row(row, subscription)
            else:
                display_error_message(f"Payment with ID {payment_id} not found")
                return None
                
        except Exception as e:
            display_error_message(f"Error retrieving payment: {str(e)}")
            return None

    def get_payments_by_subscription(self, subscription_id: int) -> List[Payment]:

        try:
            query = """
                SELECT p.*, 
                s.member_id, s.plan_id, s.start_date, s.end_date, s.is_active,
                m.first_name, m.last_name, m.email, m.phone, m.date_joined, m.status,
                pl.name as plan_name, pl.description, pl.duration_days, pl.price, pl.is_active as plan_is_active
                FROM payments p
                JOIN subscriptions s ON p.subscription_id = s.id
                JOIN members m ON s.member_id = m.id
                JOIN plans pl ON s.plan_id = pl.id
                WHERE p.subscription_id = ?
                ORDER BY p.payment_date DESC, p.id DESC
            """
            rows = execute_query(query, (subscription_id,))
            
            payments = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)                
                payment = self._create_payment_from_row(row, subscription)
                payments.append(payment)
                
            return payments
            
        except Exception as e:
            display_error_message(f"Error retrieving subscription payments: {str(e)}")
            return []

    def get_payments_by_member(self, member_id: int) -> List[Payment]:

        try:
            query = """
                SELECT p.*, 
                s.member_id, s.plan_id, s.start_date, s.end_date, s.is_active,
                m.first_name, m.last_name, m.email, m.phone, m.date_joined, m.status,
                pl.name as plan_name, pl.description, pl.duration_days, pl.price, pl.is_active as plan_is_active
                FROM payments p
                JOIN subscriptions s ON p.subscription_id = s.id
                JOIN members m ON s.member_id = m.id
                JOIN plans pl ON s.plan_id = pl.id
                WHERE s.member_id = ?
                ORDER BY p.payment_date DESC, p.id DESC
            """
            rows = execute_query(query, (member_id,))
            
            payments = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)                
                payment = self._create_payment_from_row(row, subscription)
                payments.append(payment)
                
            return payments
            
        except Exception as e:
            display_error_message(f"Error retrieving member payments: {str(e)}")
            return []

    def get_payments_by_date_range(self, start_date: str, end_date: str) -> List[Payment]:
        
        # Validate date range
        is_valid, error_msg = validate_payment_date_range(start_date, end_date)
        if not is_valid:
            display_error_message(error_msg)
            return []
            
        try:
            query = """
                SELECT p.*, 
                s.member_id, s.plan_id, s.start_date, s.end_date, s.is_active,
                m.first_name, m.last_name, m.email, m.phone, m.date_joined, m.status,
                pl.name as plan_name, pl.description, pl.duration_days, pl.price, pl.is_active as plan_is_active
                FROM payments p
                JOIN subscriptions s ON p.subscription_id = s.id
                JOIN members m ON s.member_id = m.id
                JOIN plans pl ON s.plan_id = pl.id
                WHERE p.payment_date BETWEEN ? AND ?
                ORDER BY p.payment_date DESC, p.id DESC
            """
            rows = execute_query(query, (start_date, end_date))
            
            payments = []
            for row in rows:
                member = self._create_member_from_row(row)
                plan = self._create_plan_from_row(row)
                subscription = self._create_subscription_from_row(row, member, plan)                
                payment = self._create_payment_from_row(row, subscription)
                payments.append(payment)
                
            return payments
            
        except Exception as e:
            display_error_message(f"Error retrieving payments by date range: {str(e)}")
            return []

    def get_todays_payments(self) -> List[Payment]:
        try:
            today = get_current_date()
            return self.get_payments_by_date_range(today, today)
        except Exception as e:
            display_error_message(f"Error retrieving today's payments: {str(e)}")
            return []

    def update_payment_notes(self, payment_id:int, notes:str) -> bool:
        # Check if payment exists
        payment = self.get_payment_by_id(payment_id)
        if not payment:
            return False
            
        # Sanitize notes
        notes = notes.strip() if notes else None
            
        try:
            query = "UPDATE payments SET notes = ? WHERE id = ?"
            execute_query(query, (notes, payment_id))
            
            display_success_message(f"Payment {payment_id} notes updated successfully")
            return True
            
        except Exception as e:
            display_error_message(f"Error updating payment notes: {str(e)}")
            return False

    def get_payment_stats(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        try:
            if start_date and end_date:
                # Validate date range
                is_valid, error_msg = validate_date_ranges(start_date, end_date)
                if not is_valid:
                    display_error_message(error_msg)
                    return {}
                    
                query_total = """
                    SELECT COUNT(*) as count, SUM(amount) as total 
                    FROM payments 
                    WHERE payment_date BETWEEN ? AND ?
                """
                result = execute_query(query_total, (start_date, end_date))[0]
            else:
                query_total = "SELECT COUNT(*) as count, SUM(amount) as total FROM payments"
                result = execute_query(query_total)[0]
            
            count = result['count'] if result else 0
            total = result['total'] if result and result['total'] else 0.0
            
            return {
                'total_payments': count,
                'total_revenue': total,
                'average_payment': total / count if count > 0 else 0
            }
            
        except Exception as e:
            display_error_message(f"Error retrieving payment statistics: {str(e)}")
            return {
                'total_payments': 0,
                'total_revenue': 0.0,
                'average_payment': 0.0
            }

# Singleton instance for use throughout the application
payment_manager = PaymentManager()

# Import managers at the end to avoid circular imports