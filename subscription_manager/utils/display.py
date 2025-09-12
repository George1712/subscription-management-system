from typing import List, Any, Dict
from datetime import date
from .helpers import (format_currency, format_date, truncate_text,
 parse_date, days_between_dates)



def print_table(headers: List[str], rows: List[List[Any]], title: str = None) -> None:
    if not headers or not rows:
        print("No data to display")
        return
    
    # Calculate column widths
    col_widths = []
    for i in range(len(headers)):
        max_width = len(str(headers[i]))
        for row in rows:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)  # Add some padding
    
    # Print title
    if title:
        total_width = sum(col_widths) + len(col_widths) - 1
        print(f"\n{title.upper()}")
        print("=" * total_width)
    
    # Print headers
    header_row = ""
    for i, header in enumerate(headers):
        header_row += f"{header:<{col_widths[i]}}"
    print(header_row)
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        row_str = ""
        for i, cell in enumerate(row):
            if i < len(col_widths):
                row_str += f"{str(cell):<{col_widths[i]}}"
        print(row_str)



def display_members_table(members: List[Any]) -> None:

    headers = ["ID", "Name", "Email", "Phone", "Join Date", "Status"]
    rows = []

    for member in members :
        rows.append([
            member.id,
            f"{member.first_name} {member.last_name}",
            member.email or "N/A",
            member.phone or "N/A",
            format_date(member.date_joined),
            member.status
        ])

    print_table(headers, rows, "Members")


def display_plans_table(plans: List[Any]) -> None :

    headers = ["ID", "Name", "Description", "Duration", "Price", "Active"]
    rows = []

    for plan in plans :
        rows.append([
            plan.id,
            plan.name,
            truncate_text(plan.description or "", 30),
            f"{plan.duration_days} days",
            format_currency(plan.price),
            "Yes" if plan.is_active else "No"

        ])

    print_table(headers, rows, "Subscription Plans")


def display_subscriptions_table(subscriptions: List[Any]) -> None:

    headers = ["ID", "Member", "Plan", "Start Date", "End Date", "Status", "Days Left"]
    rows = []
    
    for sub in subscriptions:
        member_name = f"{sub.member.first_name} {sub.member.last_name}" if sub.member else f"Member #{sub.member_id}"
        plan_name = sub.plan.name if sub.plan else f"Plan #{sub.plan_id}"
        days_left = sub.remaining_days()
        
        rows.append([
            sub.id,
            truncate_text(member_name, 20),
            truncate_text(plan_name, 15),
            format_date(sub.start_date),
            format_date(sub.end_date),
            "Active" if sub.is_active else "Inactive",
            days_left
        ])
    
    print_table(headers, rows, "Subscriptions")


def display_payments_table(payments: List[Any]) -> None:
    headers = ["ID", "Subscription ID", "Amount", "Payment Date", "Notes"]
    rows = []
    
    for payment in payments:
        rows.append([
            payment.id,
            payment.subscription_id,
            format_currency(payment.amount),
            format_date(payment.payment_date),
            truncate_text(payment.notes or "", 30)
        ])
    
    print_table(headers, rows, "Payments")




def display_member_details(member: Any) -> None :
    print("\n" + "=" * 50)
    print("MEMBER DETAILS")
    print("=" * 50)
    print(f"ID: {member.id}")
    print(f"Name: {member.first_name} {member.last_name}")
    print(f"Email: {member.email or 'N/A'}")
    print(f"Phone: {member.phone or 'N/A'}")
    print(f"Join Date: {format_date(member.date_joined)}")
    print(f"Status: {member.status}")
    print("=" * 50)

def display_plan_details(plan: Any) -> None:
    print("\n" + "=" * 50)
    print("PLAN DETAILS")
    print("=" * 50)
    print(f"ID: {plan.id}")
    print(f"Name: {plan.name}")
    print(f"Description: {plan.description or 'N/A'}")
    print(f"Duration: {plan.duration_days} days")
    print(f"Price: {format_currency(plan.price)}")
    print(f"Active: {'Yes' if plan.is_active else 'No'}")
    print("=" * 50)

def display_subscription_details(subscription: Any) -> None:
    print("\n" + "=" * 50)
    print("SUBSCRIPTION DETAILS")
    print("=" * 50)
    print(f"ID: {subscription.id}")
    print(f"Member: {subscription.member.first_name} {subscription.member.last_name}")
    print(f"Plan: {subscription.plan.name}")
    print(f"Start Date: {format_date(subscription.start_date)}")
    print(f"End Date: {format_date(subscription.end_date)}")
    print(f"Status: {'Active' if subscription.is_active else 'Inactive'}")
    print(f"Days Remaining: {subscription.remaining_days()}")
    print("=" * 50)



# Menu display functions

def display_main_menu() -> None:
    print("\n" + "=" * 30)
    print("SUBSCRIPTION MANAGEMENT SYSTEM")
    print("=" * 30)
    print("1. Member Management")
    print("2. Subscription Plans")
    print("3. Subscription Operations")
    print("4. Payment Processing")
    print("5. Reports & Analytics")
    print("6. Exit")
    print("=" * 30)

def display_member_management_menu() -> None:
    print("\n--- Member Management ---")
    print("1. Add New Member")
    print("2. View All Members")
    print("3. Search Member by ID")
    print("4. Search Member by Name")
    print("5. Update Member Information")
    print("6. Deactivate/Reactivate Member")
    print("7. Back to Main Menu")

def display_plan_management_menu() -> None:
    print("\n--- Subscription Plans ---")
    print("1. Create New Plan")
    print("2. View All Plans")
    print("3. Update Plan Details")
    print("4. Deactivate Plan")
    print("5. Back to Main Menu")

def display_subscription_menu() -> None:
    print("\n--- Subscription Operations ---")
    print("1. Assign Plan to Member")
    print("2. View All Active Subscriptions")
    print("3. Check Member Subscription Status")
    print("4. Renew Subscription")
    print("5. Cancel Subscription")
    print("6. Back to Main Menu")

def display_payment_menu() -> None:
    print("\n--- Payment Processing ---")
    print("1. Record Payment")
    print("2. View Payment History for Member")
    print("3. View Today's Payments")
    print("4. View Payments by Date Range")
    print("5. Back to Main Menu")

def display_reports_menu() -> None:
    print("\n--- Reports & Analytics ---")
    print("1. System Summary")
    print("2. Active Members Report")
    print("3. Expiring Subscriptions (Next 7 days)")
    print("4. Expired Subscriptions")
    print("5. Revenue Report")
    print("6. Plan Popularity Report")
    print("7. Back to Main Menu")

# Message display functions

def display_success_message(message: str) -> None:
    print(f"\n✓ SUCCESS: {message}")

def display_error_message(message: str) -> None:
    print(f"\n✗ ERROR: {message}")

def display_warning_message(message: str) -> None:
    print(f"\n⚠ WARNING: {message}")

def display_info_message(message: str) -> None:
    print(f"\nℹ INFO: {message}")



# Reports

def display_active_members_report(members: List[Any]) -> None:
    active_members = [m for m in members if m.status == "Active"]
    print(f"\nACTIVE MEMBERS REPORT: {len(active_members)} members")
    display_members_table(active_members)


def display_expiring_subscriptions_report(subscriptions: List[Any], days: int = 7) -> None:
    today = date.today()
    expiring_subs = []

    for sub in subscriptions:
        if sub.is_active :
            end_date = sub.end_date
            if isinstance(end_date, str):
                end_date = parse_date(end_date)

            days_until_expiration = days_between_dates(today, end_date)
            if 0 <= days_until_expiration <= days:
                expiring_subs.append(sub)
    
    print(f"\nSUBSCRIPTIONS EXPIRING IN THE NEXT {days} DAYS: {len(expiring_subs)} subscriptions")
    display_subscriptions_table(expiring_subs)


def display_expired_subscriptions_report(subscriptions: List[Any]) -> None:
    today = date.today()
    expired_subs = []
    
    for sub in subscriptions:
        if sub.is_active:
            end_date = sub.end_date
            if isinstance(end_date, str):
                end_date = parse_date(end_date)
            if end_date < today:
                expired_subs.append(sub)
    
    print(f"\nEXPIRED SUBSCRIPTIONS: {len(expired_subs)} subscriptions")
    display_subscriptions_table(expired_subs)


def display_revenue_report(payments: List[Any], period: str = "month") -> None:
    total_revenue = sum(p.amount for p in payments)
    print(f"\nREVENUE REPORT ({period.upper()}): {format_currency(total_revenue)}")
    display_payments_table(payments)


def display_plan_popularity_report(plans_with_stats: List[Any]) -> None:
    headers = ["Plan ID", "Plan Name", "Active Subscriptions", "Total Revenue"]
    rows = []
    
    for plan_stat in plans_with_stats:
        rows.append([
            plan_stat.plan_id,
            plan_stat.plan_name,
            plan_stat.active_subscriptions,
            format_currency(plan_stat.total_revenue)
        ])
    
    print_table(headers, rows, "Plan Popularity Report")



def display_summary_stats(stats: Dict[str, int]) -> None:
    print("\n" + "=" * 30)
    print("SYSTEM SUMMARY")
    print("=" * 30)
    print(f"Total Members: {stats.get('total_members', 0)}")
    print(f"Active Members: {stats.get('active_members', 0)}")
    print(f"Total Subscriptions: {stats.get('total_subscriptions', 0)}")
    print(f"Active Subscriptions: {stats.get('active_subscriptions', 0)}")
    print(f"Monthly Revenue: {format_currency(stats.get('monthly_revenue', 0))}")
    print("=" * 30)