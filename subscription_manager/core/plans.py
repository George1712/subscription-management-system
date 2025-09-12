from typing import List, Optional, Dict, Any
from ..models import Plan
from ..database import execute_query, execute_insert
from ..utils.validators import validate_positive_number, validate_name
from ..utils.helpers import sanitize_input, format_currency
from ..utils.display import (display_plans_table, display_plan_details, 
 display_success_message, display_error_message)


class PlanManager :
    def __init__(self) :
        pass
    
    def add_plan(self, name:str, description:str, duration_days:int,
                 price:float, is_active:bool = True) -> Optional[Plan] :

        name = sanitize_input(name)
        description = sanitize_input(description) if description else None

        is_valid, error_msg = validate_name(name, "Plan name")
        if not is_valid:
            display_error_message(error_msg)
            return None
            
        is_valid, error_msg = validate_positive_number(duration_days, "Duration", allow_zero=False)
        if not is_valid:
            display_error_message(error_msg)
            return None

        is_valid, error_msg = validate_positive_number(price, "Price", allow_zero=True)
        if not is_valid:
            display_error_message(error_msg)
            return None

        try :
            query = """
                INSERT INTO plans (name, description, duration_days, price, is_active)
                VALUES (?, ?, ?, ?, ?)
            """
            plan_id = execute_insert(query, (name, description, duration_days, price, is_active))

            if plan_id :
                plan = Plan(
                    id = plan_id,
                    name = name,
                    description = description,
                    duration_days = duration_days,
                    price = price,
                    is_active = is_active
                )
                display_success_message(f"Plan '{name}' added successfully with ID: {plan_id}")
                return plan
            else :
                display_error_message("Failed to add plan to database")
                return None
        except Exception as e:
            display_error_message(f"Error adding plan: {str(e)}")
            return None
    

    def get_all_plans(self, include_inactive:bool = False) -> List[Plan] :
        try:
            if include_inactive:
                query = "SELECT * FROM plans ORDER BY id"
            else:
                query = "SELECT * FROM plans WHERE is_active = TRUE ORDER BY id"
                
            rows = execute_query(query)
            
            plans = []
            for row in rows:
                plans.append(Plan.from_db_row(row))
                
            return plans
            
        except Exception as e:
            display_error_message(f"Error retrieving plans: {str(e)}")
            return []

    

    def get_plan_by_id(self, plan_id:int) -> Optional[Plan] :
        try :
            query = "SELECT * FROM plans WHERE id = ?"
            rows = execute_query(query, (plan_id,))

            if rows : 
                return Plan.from_db_row(rows[0])
            else :
                display_error_message(f"Plan with ID {plan_id} not found")
                return None
        except Exception as e :
            display_error_message(f"Error retrieving plan: {str(e)}")
            return None
        
    def update_plan_name(self, plan_id:int, name:str) -> bool :
        if self.get_plan_by_id(plan_id) is None :
            display_error_message(f"Plan with id {plan_id} doesn't exist")
            return False

        name = sanitize_input(name)
        is_valid, error_msg = validate_name(name, "Plan name")
        if not is_valid :
            display_error_message(error_msg)
            return False
        
        try :
            query = "UPDATE plans SET name = ? WHERE id = ?"
            execute_query(query, (name, plan_id))
            display_success_message(f"Plan {plan_id} name updated successfully")
            return True
        except Exception as e :
            display_error_message(f"Error updating plan name: {str(e)}")
            return False
    

    def update_plan_description(self, plan_id:int, description:str) -> bool :
        if self.get_plan_by_id(plan_id) is None :
            display_error_message(f"Plan with id {plan_id} doesn't exist")
            return False

        description = sanitize_input(description) if description else None

        try:
            query = "UPDATE plans SET description = ? WHERE id = ?"
            execute_query(query, (description, plan_id))
            display_success_message(f"Plan {plan_id} description updated successfully")
            return True
            
        except Exception as e:
            display_error_message(f"Error updating plan description: {str(e)}")
            return False


    def update_plan_duration(self, plan_id: int, duration_days: int) -> bool:
        if self.get_plan_by_id(plan_id) is None :
            display_error_message(f"Plan with id {plan_id} doesn't exist")
            return False

        is_valid, error_msg = validate_positive_number(duration_days, "Duration", allow_zero=False)
        if not is_valid:
            display_error_message(error_msg)
            return False
            
        try:
            query = "UPDATE plans SET duration_days = ? WHERE id = ?"
            execute_query(query, (duration_days, plan_id))
            display_success_message(f"Plan {plan_id} duration updated to {duration_days} days")
            return True
            
        except Exception as e:
            display_error_message(f"Error updating plan duration: {str(e)}")
            return False


            
    def update_plan_price(self, plan_id: int, price: float) -> bool:
        if self.get_plan_by_id(plan_id) is None :
            display_error_message(f"Plan with id {plan_id} doesn't exist")
            return False
            
        is_valid, error_msg = validate_positive_number(price, "Price", allow_zero=False)
        if not is_valid:
            display_error_message(error_msg)
            return False
            
        try:
            query = "UPDATE plans SET price = ? WHERE id = ?"
            execute_query(query, (price, plan_id))
            display_success_message(f"Plan {plan_id} price updated to {format_currency(price)}")
            return True
            
        except Exception as e:
            display_error_message(f"Error updating plan price: {str(e)}")
            return False

    def set_plan_status(self, plan_id: int, is_active: bool) -> bool:
        try:
            query = "UPDATE plans SET is_active = ? WHERE id = ?"
            execute_query(query, (is_active, plan_id))
            
            status_text = "activated" if is_active else "deactivated"
            display_success_message(f"Plan {plan_id} {status_text} successfully")
            return True
            
        except Exception as e:
            display_error_message(f"Error updating plan status: {str(e)}")
            return False
    
    def activate_plan(self, plan_id: int) -> bool:
        return self.set_plan_status(plan_id, True)

    def deactivate_plan(self, plan_id: int) -> bool:
        return self.set_plan_status(plan_id, False)

    def get_plan_stats(self):
        try:
            query = """
                SELECT 
                    p.id as plan_id,
                    p.name as plan_name,
                    COUNT(DISTINCT s.id) as total_subscriptions,
                    SUM(CASE WHEN s.is_active THEN 1 ELSE 0 END) as active_subscriptions,
                    COALESCE(SUM(pm.amount), 0) as total_revenue
                FROM plans p
                LEFT JOIN subscriptions s ON p.id = s.plan_id
                LEFT JOIN payments pm ON s.id = pm.subscription_id
                GROUP BY p.id, p.name
                ORDER BY p.id
            """
            rows = execute_query(query)
            return rows
        except Exception as e:
            display_error_message(f"Error retrieving plan statistics: {str(e)}")
            return []

# Singleton instance
plan_manager = PlanManager()