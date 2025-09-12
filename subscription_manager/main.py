import sys
import os
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from subscription_manager import (
    member_manager,
    plan_manager,
    subscription_manager,
    payment_manager
)
from subscription_manager.utils import (
    clear_screen, press_enter_to_continue, get_confirmation, is_valid_id, format_currency,
    validate_date, validate_positive_number, validate_name, validate_email, validate_phone,
    display_main_menu, display_success_message, display_error_message, display_info_message,
    display_warning_message, display_member_management_menu, display_member_details,
    display_members_table, display_plan_management_menu, display_plan_details,
    display_plans_table, display_subscription_menu, display_subscription_details,
    display_subscriptions_table, display_payment_menu, display_payments_table,
    display_reports_menu, print_table
)


class SubscriptionManagementSystem :
    
    def __init__(self):
        self.running = True
        self.current_user = None
    
    def run(self):
        """Main application loop"""
        clear_screen()
        self.display_welcome()
        
        while self.running:
            try:
                display_main_menu()
                choice = input("\nEnter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.member_management_menu()
                elif choice == '2':
                    self.plan_management_menu()
                elif choice == '3':
                    self.subscription_management_menu()
                elif choice == '4':
                    self.payment_management_menu()
                elif choice == '5':
                    self.reports_menu()
                elif choice == '6':
                    self.exit_application()
                else:
                    display_error_message("Invalid choice. Please enter 1-6.")
                    press_enter_to_continue()
                    
            except KeyboardInterrupt:
                self.exit_application()
            except Exception as e:
                display_error_message(f"An unexpected error occurred: {str(e)}")
                press_enter_to_continue()
    
    def display_welcome(self):
        """Display welcome message and system status"""
        print("=" * 60)
        print("    WELCOME TO SUBSCRIPTION MANAGEMENT SYSTEM")
        print("=" * 60)
        
        # Display system summary
        try:
            members = member_manager.get_all_members()
            plans = plan_manager.get_all_plans()
            subscriptions = subscription_manager.get_all_subscriptions()
            payment_stats = payment_manager.get_payment_stats()
            
            print(f"\nSystem Status:")
            print(f"  • Members: {len(members)}")
            print(f"  • Plans: {len(plans)}")
            print(f"  • Subscriptions: {len(subscriptions)}")
            print(f"  • Total Revenue: {format_currency(payment_stats.get('total_revenue', 0))}")
            
        except Exception as e:
            display_error_message(f"Error loading system status: {str(e)}")
        
        press_enter_to_continue()
    
    def member_management_menu(self):
        while True:
            clear_screen()
            display_member_management_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.view_all_members()
            elif choice == '3':
                self.search_member_by_id()
            elif choice == '4':
                self.search_member_by_name()
            elif choice == '5':
                self.update_member_info()
            elif choice == '6':
                self.update_member_status()
            elif choice == '7':
                break
            else:
                display_error_message("Invalid choice. Please enter 1-7.")
                press_enter_to_continue()
    
    def add_member(self):
        clear_screen()
        print("ADD NEW MEMBER")
        print("=" * 30)
        
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email (optional): ").strip() or None
        phone = input("Phone (optional): ").strip() or None
        
        member = member_manager.add_member(first_name, last_name, email, phone)
        if member:
            display_member_details(member)
        
        press_enter_to_continue()
    
    def view_all_members(self):
        clear_screen()
        members = member_manager.get_all_members()
        
        if not members:
            display_info_message("No members found in the system.")
        else:
            display_members_table(members)
        
        press_enter_to_continue()
    
    def search_member_by_id(self):
        clear_screen()
        print("SEARCH MEMBER BY ID")
        print("=" * 25)
        
        try:
            member_id = int(input("Enter Member ID: ").strip())
            member = member_manager.get_member_by_id(member_id)
            if member:
                display_member_details(member)
            press_enter_to_continue()
        except ValueError:
            display_error_message("Invalid Member ID format")
            press_enter_to_continue()
    
    def search_member_by_name(self):
        clear_screen()
        print("SEARCH MEMBERS BY NAME")
        print("=" * 28)
        
        name = input("Enter name to search: ").strip()
        
        if not name:
            display_error_message("Please enter a name to search.")
        else:
            members = member_manager.get_members_by_name(name)
            if members:
                display_members_table(members)
            else:
                display_info_message(f"No members found matching '{name}'.")
        
        press_enter_to_continue()
    
    def update_member_info(self):
        clear_screen()
        print("UPDATE MEMBER INFORMATION")
        print("=" * 32)
        
        member_id = input("Enter Member ID: ").strip()
        
        if not is_valid_id(member_id):
            display_error_message("Invalid member ID format.")
            press_enter_to_continue()
            return
        
        member = member_manager.get_member_by_id(int(member_id))
        if not member:
            display_error_message(f"Member with ID {member_id} not found.")
            press_enter_to_continue()
            return
        
        display_member_details(member)
        
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Email")
        print("3. Phone")
        print("4. Cancel")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            new_first = input(f"New First Name (current: {member.first_name}): ").strip() or member.first_name
            new_last = input(f"New Last Name (current: {member.last_name}): ").strip() or member.last_name
            member_manager.update_member_name(member.id, new_first, new_last)
        
        elif choice == '2':
            new_email = input(f"New Email (current: {member.email or 'None'}): ").strip() or None
            member_manager.update_member_email(member.id, new_email)
        
        elif choice == '3':
            new_phone = input(f"New Phone (current: {member.phone or 'None'}): ").strip() or None
            member_manager.update_member_phone(member.id, new_phone)
        
        elif choice == '4':
            return
        else:
            display_error_message("Invalid choice.")
        
        press_enter_to_continue()
    
    def update_member_status(self):
        clear_screen()
        print("UPDATE MEMBER STATUS")
        print("=" * 25)
        
        member_id = input("Enter Member ID: ").strip()
        
        if not is_valid_id(member_id):
            display_error_message("Invalid member ID format.")
            press_enter_to_continue()
            return
        
        member = member_manager.get_member_by_id(int(member_id))
        if not member:
            display_error_message(f"Member with ID {member_id} not found.")
            press_enter_to_continue()
            return
        
        display_member_details(member)
        
        new_status = "Inactive" if member.status == "Active" else "Active"
        
        if get_confirmation(f"Change status to '{new_status}'?"):
            member_manager.update_member_status(member.id, new_status)
        
        press_enter_to_continue()
    

    def plan_management_menu(self):
        while True:
            clear_screen()
            display_plan_management_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.create_plan()
            elif choice == '2':
                self.view_all_plans()
            elif choice == '3':
                self.update_plan_details()
            elif choice == '4':
                self.deactivate_plan()
            elif choice == '5':
                break
            else:
                display_error_message("Invalid choice. Please enter 1-5.")
                press_enter_to_continue()
    
    def create_plan(self):
        clear_screen()
        print("CREATE NEW SUBSCRIPTION PLAN")
        print("=" * 35)
        
        name = input("Plan Name: ").strip()
        description = input("Description (optional): ").strip() or None
        duration_input = input("Duration in days: ").strip()
        price_input = input("Price: ").strip()
        
        # Validate duration
        try:
            duration_days = int(duration_input) if duration_input else 0
        except ValueError:
            duration_days = 0 
        
        # Validate price
        try:
            price = float(price_input) if price_input else 0
        except ValueError:
            price = 0  # Let add_plan handle the validation
        
        plan = plan_manager.add_plan(name, description, int(duration_input), price)
        if plan:
            display_plan_details(plan)
        
        press_enter_to_continue()
    
    def view_all_plans(self):
        clear_screen()
        plans = plan_manager.get_all_plans(include_inactive=True)
        
        if not plans:
            display_info_message("No plans found in the system.")
        else:
            display_plans_table(plans)
        
        press_enter_to_continue()
    
    def update_plan_details(self):
        clear_screen()
        print("UPDATE PLAN DETAILS")
        print("=" * 25)
        
        plan_id = input("Enter Plan ID: ").strip()
        
        if not is_valid_id(plan_id):
            display_error_message("Invalid plan ID format.")
            press_enter_to_continue()
            return
        
        plan = plan_manager.get_plan_by_id(int(plan_id))
        if not plan:
            display_error_message(f"Plan with ID {plan_id} not found.")
            press_enter_to_continue()
            return
        
        display_plan_details(plan)
        
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Description")
        print("3. Duration")
        print("4. Price")
        print("5. Cancel")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            new_name = input(f"New Name (current: {plan.name}): ").strip()
            if new_name:
                plan_manager.update_plan_name(plan.id, new_name)
        
        elif choice == '2':
            new_desc = input(f"New Description (current: {plan.description or 'None'}): ").strip() or None
            plan_manager.update_plan_description(plan.id, new_desc)
        
        elif choice == '3':
            new_duration = input(f"New Duration in days (current: {plan.duration_days}): ").strip()
            if new_duration and new_duration.isdigit():
                plan_manager.update_plan_duration(plan.id, int(new_duration))
            else:
                display_error_message("Duration must be a positive integer.")
        
        elif choice == '4':
            new_price = input(f"New Price (current: {format_currency(plan.price)}): ").strip()
            try:
                if new_price:
                    price = float(new_price)
                    plan_manager.update_plan_price(plan.id, price)
            except ValueError:
                display_error_message("Price must be a valid number.")
        
        elif choice == '5':
            return
        else:
            display_error_message("Invalid choice.")
        
        press_enter_to_continue()
    
    def deactivate_plan(self):
        clear_screen()
        print("DEACTIVATE PLAN")
        print("=" * 20)
        
        plan_id = input("Enter Plan ID: ").strip()
        
        if not is_valid_id(plan_id):
            display_error_message("Invalid plan ID format.")
            press_enter_to_continue()
            return
        
        plan = plan_manager.get_plan_by_id(int(plan_id))
        if not plan:
            display_error_message(f"Plan with ID {plan_id} not found.")
            press_enter_to_continue()
            return
        
        display_plan_details(plan)
        
        if plan.is_active:
            if get_confirmation("Deactivate this plan?"):
                plan_manager.deactivate_plan(plan.id)
        else:
            if get_confirmation("Activate this plan?"):
                plan_manager.activate_plan(plan.id)
        
        press_enter_to_continue()
    
    def subscription_management_menu(self):
        while True:
            clear_screen()
            display_subscription_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.assign_plan_to_member()
            elif choice == '2':
                self.view_all_subscriptions()
            elif choice == '3':
                self.check_member_subscription_status()
            elif choice == '4':
                self.renew_subscription()
            elif choice == '5':
                self.cancel_subscription()
            elif choice == '6':
                break
            else:
                display_error_message("Invalid choice. Please enter 1-6.")
                press_enter_to_continue()
    
    def assign_plan_to_member(self):
        clear_screen()
        print("ASSIGN PLAN TO MEMBER")
        print("=" * 28)
        
        # Get member
        member_id = input("Enter Member ID: ").strip()
        if not is_valid_id(member_id):
            display_error_message("Invalid member ID format.")
            press_enter_to_continue()
            return
        
        member = member_manager.get_member_by_id(int(member_id))
        if not member:
            display_error_message(f"Member with ID {member_id} not found.")
            press_enter_to_continue()
            return
        
        display_member_details(member)
        
        # Get plan
        plan_id = input("\nEnter Plan ID: ").strip()
        if not is_valid_id(plan_id):
            display_error_message("Invalid plan ID format.")
            press_enter_to_continue()
            return
        
        plan = plan_manager.get_plan_by_id(int(plan_id))
        if not plan:
            display_error_message(f"Plan with ID {plan_id} not found.")
            press_enter_to_continue()
            return
        
        display_plan_details(plan)
        
        # Get start date
        start_date = input(f"\nStart date (YYYY-MM-DD, leave empty for today): ").strip()
        
        subscription = subscription_manager.create_subscription(
            member.id, plan.id, start_date or None
        )
        
        if subscription:
            display_subscription_details(subscription)
        
        press_enter_to_continue()
    
    def view_all_subscriptions(self):
        clear_screen()
        subscriptions = subscription_manager.get_all_subscriptions(include_inactive=True)
        
        if not subscriptions:
            display_info_message("No subscriptions found in the system.")
        else:
            display_subscriptions_table(subscriptions)
        
        press_enter_to_continue()
    
    def check_member_subscription_status(self):
        clear_screen()
        print("CHECK MEMBER SUBSCRIPTION STATUS")
        print("=" * 38)
        
        member_id = input("Enter Member ID: ").strip()
        
        if not is_valid_id(member_id):
            display_error_message("Invalid member ID format.")
            press_enter_to_continue()
            return
        
        member = member_manager.get_member_by_id(int(member_id))
        if not member:
            display_error_message(f"Member with ID {member_id} not found.")
            press_enter_to_continue()
            return
        
        display_member_details(member)
        
        subscriptions = subscription_manager.get_subscriptions_by_member(member.id)
        
        if subscriptions:
            print(f"\nSubscriptions for {member.first_name} {member.last_name}:")
            display_subscriptions_table(subscriptions)
        else:
            display_info_message("No subscriptions found for this member.")
        
        press_enter_to_continue()
    
    def renew_subscription(self):
        clear_screen()
        print("RENEW SUBSCRIPTION")
        print("=" * 22)
        
        subscription_id = input("Enter Subscription ID: ").strip()
        
        if not is_valid_id(subscription_id):
            display_error_message("Invalid subscription ID format.")
            press_enter_to_continue()
            return
        
        subscription = subscription_manager.get_subscription_by_id(int(subscription_id))
        if not subscription:
            display_error_message(f"Subscription with ID {subscription_id} not found.")
            press_enter_to_continue()
            return
        
        display_subscription_details(subscription)
        
        if get_confirmation("Renew this subscription?"):
            subscription_manager.renew_subscription(subscription.id)
        
        press_enter_to_continue()
    
    def cancel_subscription(self):
        clear_screen()
        print("CANCEL SUBSCRIPTION")
        print("=" * 23)
        
        subscription_id = input("Enter Subscription ID: ").strip()
        
        if not is_valid_id(subscription_id):
            display_error_message("Invalid subscription ID format.")
            press_enter_to_continue()
            return
        
        subscription = subscription_manager.get_subscription_by_id(int(subscription_id))
        if not subscription:
            display_error_message(f"Subscription with ID {subscription_id} not found.")
            press_enter_to_continue()
            return
        
        display_subscription_details(subscription)
        
        action = "cancel" if subscription.is_active else "activate"
        
        if get_confirmation(f"{action.capitalize()} this subscription?"):
            if subscription.is_active:
                subscription_manager.cancel_subscription(subscription.id)
            else:
                subscription_manager.activate_subscription(subscription.id)
        
        press_enter_to_continue()
    
    def payment_management_menu(self):
        while True:
            clear_screen()
            display_payment_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.record_payment()
            elif choice == '2':
                self.view_payment_history_by_member()
            elif choice == '3':
                self.view_todays_payments()
            elif choice == '4':
                self.view_payments_by_date_range()
            elif choice == '5':
                break
            else:
                display_error_message("Invalid choice. Please enter 1-5.")
                press_enter_to_continue()
    
    def record_payment(self):
        clear_screen()
        print("RECORD PAYMENT")
        print("=" * 18)
        
        subscription_id = input("Enter Subscription ID: ").strip()
        
        if not is_valid_id(subscription_id):
            display_error_message("Invalid subscription ID format.")
            press_enter_to_continue()
            return
        
        subscription = subscription_manager.get_subscription_by_id(int(subscription_id))
        if not subscription:
            display_error_message(f"Subscription with ID {subscription_id} not found.")
            press_enter_to_continue()
            return
        
        display_subscription_details(subscription)
        
        amount_input = input("\nPayment Amount: ").strip()
        try:
            amount = float(amount_input)
        except ValueError:
            display_error_message("Amount must be a valid number.")
            press_enter_to_continue()
            return
        
        payment_date = input("Payment Date (YYYY-MM-DD, leave empty for today): ").strip() or None
        notes = input("Notes (optional): ").strip() or None
        
        payment = payment_manager.record_payment(
            subscription.id, amount, payment_date, notes
        )
        
        if payment:
            print(f"\nPayment recorded successfully!")
            print(f"Payment ID: {payment.id}")
            print(f"Amount: {format_currency(payment.amount)}")
            print(f"Date: {payment.payment_date}")
        
        press_enter_to_continue()
    
    def view_payment_history_by_member(self):
        clear_screen()
        print("PAYMENT HISTORY BY MEMBER")
        print("=" * 30)
        
        member_id = input("Enter Member ID: ").strip()
        
        if not is_valid_id(member_id):
            display_error_message("Invalid member ID format.")
            press_enter_to_continue()
            return
        
        member = member_manager.get_member_by_id(int(member_id))
        if not member:
            display_error_message(f"Member with ID {member_id} not found.")
            press_enter_to_continue()
            return
        
        display_member_details(member)
        
        payments = payment_manager.get_payments_by_member(member.id)
        
        if payments:
            print(f"\nPayment History for {member.first_name} {member.last_name}:")
            display_payments_table(payments)
            
            total = sum(p.amount for p in payments)
            print(f"\nTotal Payments: {format_currency(total)}")
        else:
            display_info_message("No payments found for this member.")
        
        press_enter_to_continue()
    
    def view_todays_payments(self):
        clear_screen()
        print("TODAY'S PAYMENTS")
        print("=" * 20)
        
        payments = payment_manager.get_todays_payments()
        
        if payments:
            display_payments_table(payments)

            total = sum(p.amount for p in payments)
            print(f"\nToday's Total: {format_currency(total)}")
        else:
            display_info_message("No payments recorded today.")
        
        press_enter_to_continue()
    
    def view_payments_by_date_range(self):
        clear_screen()
        print("PAYMENTS BY DATE RANGE")
        print("=" * 27)
        
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        
        payments = payment_manager.get_payments_by_date_range(start_date, end_date)
        
        if payments:
            display_payments_table(payments)
            
            total = sum(p.amount for p in payments)
            print(f"\nTotal for period: {format_currency(total)}")
        else:
            display_info_message(f"No payments found between {start_date} and {end_date}.")
        
        press_enter_to_continue()
    
    def reports_menu(self):
        while True:
            clear_screen()
            display_reports_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.system_summary()
            elif choice == '2':
                self.active_members_report()
            elif choice == '3':
                self.expiring_subscriptions_report()
            elif choice == '4':
                self.expired_subscriptions_report()
            elif choice == '5':
                self.revenue_report()
            elif choice == '6':
                self.plan_popularity_report()
            elif choice == '7':
                break
            else:
                display_error_message("Invalid choice. Please enter 1-7.")
                press_enter_to_continue()
    
    def system_summary(self):
        clear_screen()
        print("SYSTEM SUMMARY")
        print("=" * 18)
        
        try:
            # Get basic counts
            members = member_manager.get_all_members()
            plans = plan_manager.get_all_plans()
            subscriptions = subscription_manager.get_all_subscriptions()
            payment_stats = payment_manager.get_payment_stats()
            subscription_stats = subscription_manager.get_subscription_stats()
            
            active_members = len([m for m in members if m.status == "Active"])
            
            print(f"\nSystem Overview:")
            print(f"  Total Members: {len(members)}")
            print(f"  Active Members: {active_members}")
            print(f"  Total Plans: {len(plans)}")
            print(f"  Total Subscriptions: {subscription_stats.get('total_subscriptions', 0)}")
            print(f"  Active Subscriptions: {subscription_stats.get('active_subscriptions', 0)}")
            print(f"  Expired Subscriptions: {subscription_stats.get('expired_subscriptions', 0)}")
            print(f"  Expiring Soon (7 days): {subscription_stats.get('expiring_subscriptions', 0)}")
            print(f"  Total Revenue: {format_currency(payment_stats.get('total_revenue', 0))}")
            print(f"  Average Payment: {format_currency(payment_stats.get('average_payment', 0))}")
            
        except Exception as e:
            display_error_message(f"Error generating system summary: {str(e)}")
        
        press_enter_to_continue()
    
    def active_members_report(self):
        clear_screen()
        print("ACTIVE MEMBERS REPORT")
        print("=" * 25)
        
        members = member_manager.get_all_members()
        active_members = [m for m in members if m.status == "Active"]
        
        if active_members:
            display_members_table(active_members)
        else:
            display_info_message("No active members found.")
        
        press_enter_to_continue()
    
    def expiring_subscriptions_report(self):
        clear_screen()
        print("EXPIRING SUBSCRIPTIONS REPORT")
        print("=" * 35)
        
        days = input("Days ahead to check (default 7): ").strip()
        try:
            days = int(days) if days else 7
        except ValueError:
            days = 7
        
        subscriptions = subscription_manager.get_expiring_subscriptions(days)
        
        if subscriptions:
            print(f"\nSubscriptions expiring in the next {days} days:")
            display_subscriptions_table(subscriptions)
        else:
            display_info_message(f"No subscriptions expiring in the next {days} days.")
        
        press_enter_to_continue()
    
    def expired_subscriptions_report(self):
        clear_screen()
        print("EXPIRED SUBSCRIPTIONS REPORT")
        print("=" * 32)
        
        subscriptions = subscription_manager.get_expired_subscriptions()
        
        if subscriptions:
            display_subscriptions_table(subscriptions)
        else:
            display_info_message("No expired subscriptions found.")
        
        press_enter_to_continue()
    
    def revenue_report(self):
        clear_screen()
        print("REVENUE REPORT")
        print("=" * 18)
        
        print("Report Options:")
        print("1. All Time")
        print("2. Date Range")
        print("3. This Month")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            payments = payment_manager.get_all_payments()
            period = "All Time"
        elif choice == '2':
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            end_date = input("End Date (YYYY-MM-DD): ").strip()
            payments = payment_manager.get_payments_by_date_range(start_date, end_date)
            period = f"{start_date} to {end_date}"
        elif choice == '3':
            # Get current month
            from datetime import datetime
            now = datetime.now()
            start_date = f"{now.year}-{now.month:02d}-01"
            if now.month == 12:
                end_date = f"{now.year + 1}-01-01"
            else:
                end_date = f"{now.year}-{now.month + 1:02d}-01"
            
            payments = payment_manager.get_payments_by_date_range(start_date, end_date)
            period = f"Month of {now.strftime('%B %Y')}"
        else:
            display_error_message("Invalid choice.")
            press_enter_to_continue()
            return
        
        if payments:
            total_revenue = sum(p.amount for p in payments)
            avg_payment = total_revenue / len(payments) if payments else 0
            
            print(f"\nRevenue Report - {period}")
            print(f"Total Payments: {len(payments)}")
            print(f"Total Revenue: {format_currency(total_revenue)}")
            print(f"Average Payment: {format_currency(avg_payment)}")
            
            sorted_payments = sorted(payments, key=lambda p: p.amount, reverse=True)[:10]
            print(f"\nTop 10 Payments:")
            display_payments_table(sorted_payments)
        else:
            display_info_message(f"No payments found for {period.lower()}.")
        
        press_enter_to_continue()
    
    def plan_popularity_report(self):
        clear_screen()
        print("=== PLAN POPULARITY REPORT ===")
        
        # Get plan statistics
        plan_stats = plan_manager.get_plan_stats()
        
        if not plan_stats:
            display_info_message("No plan statistics available")
            press_enter_to_continue()
            return
        
        headers = ["Plan ID", "Plan Name", "Active Subs", "Total Subs", "Revenue"]
        rows = []
        
        for stat in plan_stats:
            rows.append([
                stat['plan_id'],
                stat['plan_name'],
                stat['active_subscriptions'],
                stat['total_subscriptions'],
                format_currency(stat['total_revenue'])
            ])
        
        print_table(headers, rows, "Plan Popularity Report")
        press_enter_to_continue()

    def exit_application(self):
        clear_screen()
        print("=" * 60)
        print("    THANK YOU FOR USING SUBSCRIPTION MANAGEMENT SYSTEM")
        print("=" * 60)
        
        self.running = False


def main():
    try:
        app = SubscriptionManagementSystem()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
