from typing import List, Optional, Dict, Any
from datetime import date
from ..models import Member
from ..database import execute_query, execute_insert
from ..utils.validators import validate_name, validate_email, validate_phone, validate_status
from ..utils.helpers import get_current_date, sanitize_input
from ..utils.display import (display_members_table, display_member_details,
 display_success_message, display_error_message)


class MemberManager :
    def __init__(self) :
        pass

    def add_member(self, first_name:str, last_name:str, email:str = None,
                    phone:str = None, date_joined:str = None) -> Optional[Member] :
        # sanitize
        first_name = sanitize_input(first_name)
        last_name = sanitize_input(last_name)
        email = sanitize_input(email)
        phone = sanitize_input(phone)
        # validate
        is_valid, error_msg = validate_name(first_name, "First name")
        if not is_valid :
            display_error_message(error_msg)
            return None

        is_valid, error_msg = validate_name(last_name, "Last name")
        if not is_valid:
            display_error_message(error_msg)
            return None
        
        if email:
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                display_error_message(error_msg)
                return None
        if phone:
            is_valid, error_msg = validate_phone(phone)
            if not is_valid:
                display_error_message(error_msg)
                return None
        
        join_date = date_joined or get_current_date()

        try :
            query = """
                INSERT INTO members(first_name, last_name, email, phone, date_joined, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            member_id = execute_insert(query, (first_name, last_name, email, phone, join_date, "Active"))
            if member_id:
                # Create and return Member object
                member = Member(
                    id = member_id,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone = phone,
                    date_joined = join_date,
                    status = "Active"
                )
                display_success_message(f"Member '{first_name} {last_name}' added successfully with ID: {member_id}")
                return member
            else:
                display_error_message("Failed to add member to database")
                return None
                
        except Exception as e:
            display_error_message(f"Error adding member: {str(e)}")
            return None

    
    def get_all_members(self) -> List[Member] :
        try :
            query = "SELECT * FROM members ORDER BY id"
            rows = execute_query(query)

            members = []
            for row in rows :
                members.append(Member.from_db_row(row))

            return members

        except Exception as e :
            display_error_message(f"Error retrieving members: {str(e)}")
            return []

    
    def get_member_by_id(self, member_id: int) -> Optional[Member] :
        try :
            query = "SELECT * FROM members WHERE id = ?"
            rows = execute_query(query, (member_id,)) 
            if rows :
                return Member.from_db_row(rows[0])
            else :
                display_error_message(f"Member with ID {member_id} not found")
                return None
        except Exception as e :
            display_error_message(f"Error retrieving member: {str(e)}")
            return None
    
    def get_members_by_name(self, name: str) -> List[Member] :

        try :
            search_term = f"%{name}%"
            query = """
                SELECT * FROM members
                WHERE first_name LIKE ? OR last_name LIKE ?
                ORDER BY id
            """
            rows = execute_query(query, (search_term, search_term))

            members = []
            for row in rows:
                members.append(Member.from_db_row(row))
                
            return members
        except Exception as e :
            display_error_message(f"Error searching members: {str(e)}")
            return []

    
    def update_member_name(self, member_id:int, first_name:str, last_name:str) -> bool :
        if not self.get_member_by_id(member_id) :
            return False

        is_valid, error_msg = validate_name(first_name, "First name")
        if not is_valid:
            display_error_message(error_msg)
            return False

        is_valid, error_msg = validate_name(last_name, "Last name")
        if not is_valid:
            display_error_message(error_msg)
            return False
        
        try :
            query = """
                UPDATE members SET first_name = ?, last_name = ?
                WHERE id = ?
            """
            execute_query(query, (first_name, last_name, member_id))
            display_success_message(f"Member {member_id} name updated successfully")
            return True
        except Exception as e :
            display_error_message(f"Error updating member name: {str(e)}")
            return False
        

    def update_member_email(self, member_id:int, email:str) -> bool:
        if not self.get_member_by_id(member_id) :
            return False
        if email:
            email = sanitize_input(email)
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                display_error_message(error_msg)
                return False
        else:
            email = None
        
        try:
            query = "UPDATE members SET email = ? WHERE id = ?"
            execute_query(query, (email, member_id))
            display_success_message(f"Member {member_id} email updated successfully")
            return True
        except Exception as e:
            display_error_message(f"Error updating member email: {str(e)}")
            return False

    def update_member_phone(self, member_id: int, phone: str) -> bool:
        if not self.get_member_by_id(member_id) :
            return False
        if phone:
            phone = sanitize_input(phone)
            is_valid, error_msg = validate_phone(phone)
            if not is_valid:
                display_error_message(error_msg)
                return False
        else:
            phone = None
        
        try:
            query = "UPDATE members SET phone = ? WHERE id = ?"
            execute_query(query, (phone, member_id))
            display_success_message(f"Member {member_id} phone updated successfully")
            return True
        except Exception as e:
            display_error_message(f"Error updating member phone: {str(e)}")
            return False


    def update_member_status(self, member_id:int, status:str) -> bool:
        if not self.get_member_by_id(member_id) :
            return False
        is_valid, error_msg = validate_status(status)
        if not is_valid:
            display_error_message(error_msg)
            return False
        
        try:
            query = "UPDATE members SET status = ? WHERE id = ?"
            execute_query(query, (status, member_id))
            display_success_message(f"Member {member_id} status updated to {status}")
            return True
        except Exception as e:
            display_error_message(f"Error updating member status: {str(e)}")
            return False

# Singleton instance
member_manager = MemberManager()