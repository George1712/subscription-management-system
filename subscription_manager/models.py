from datetime import datetime, timedelta


class Member:
    def __init__(self, id=None, first_name="", last_name="",
                 email="", phone="", date_joined=None, status="Active"):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.date_joined = date_joined or datetime.now().date()
        self.status = status
    
    def __str__(self) :
        return f"{self.first_name} {self.last_name} (ID = {self.id})"

    def to_dict(self) :
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_joined': self.date_joined.isoformat() if isinstance(self.date_joined, datetime) else self.date_joined,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data) :
        # creates a member instance from a dictionary (data)
        return cls(
            id = data.get('id'),
            first_name = data.get('first_name', ''),
            last_name = data.get('last_name', ''),
            email = data.get('email', ''),
            phone = data.get('phone', ''),
            date_joined = data.get('date_joined'),
            status = data.get('status', 'Active')
        )

    @classmethod
    def from_db_row(cls, row) :
        # creates a member instance from a dictionary (data)
        return cls(
            id = row['id'],
            first_name = row['first_name'],
            last_name = row['last_name'],
            email = row['email'],
            phone = row['phone'],
            date_joined = row['date_joined'],
            status = row['status']
        )


class Plan:
    def __init__(self, id=None, name="", description="",
                 duration_days=0, price=0.0, is_active=True) :
        self.id = id
        self.name = name
        self.description = description
        self.duration_days = duration_days
        self.price = price
        self.is_active = is_active

    def __str__(self) :
        return f"{self.name} (${self.price})"
    
    def calculate_end_date(self, start_date) :
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        return start_date + timedelta(days=self.duration_days)

    def to_dict(self) :
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration_days': self.duration_days,
            'price': self.price,
            'is_active': self.is_active
        } 
    
    @classmethod
    def from_dict(cls, data) :
        # creates a plan instance from a dictionary
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            description=data.get('description', ''),
            duration_days=data.get('duration_days', 0),
            price=data.get('price', 0.0),
            is_active=data.get('is_active', True)
        )

    @classmethod
    def from_db_row(cls, row) :
        # creates a plan instance from a database row
        return cls(
            id = row['id'],
            name = row['name'],
            description = row['description'],
            duration_days = row['duration_days'],
            price = row['price'],
            is_active = bool(row['is_active'])
        )
    

class Subscription :
    def __init__(self, id=None, member_id=None, plan_id=None, start_date=None, 
                 end_date=None, is_active=True, member=None, plan=None) :
        self.id = id
        self.member_id = member_id
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.member = member
        self.plan = plan
    
    def __str__(self) :
        return f"Subscription #{self.id} (Active: {self.is_active})"
    
    def is_currently_active(self) :
        if not self.is_active:
            return False

        today = datetime.now().date()

        if isinstance(self.start_date, str):
            start = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        else:
            start = self.start_date
        
        if isinstance(self.end_date, str):
            end = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        else:
            end = self.end_date

        return start <= today <= end

    def remaining_days(self) :
        if not self.is_active :
            return 0
        
        today = datetime.now().date()
        if isinstance(self.end_date, str):
            end = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        else:
            end = self.end_date

        if (end < today) :
            return 0
        return (end - today).days

    def to_dict(self) :
        return {
            'id': self.id,
            'member_id': self.member_id,
            'plan_id': self.plan_id,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, datetime) else self.start_date,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, datetime) else self.end_date,
            'is_active': self.is_active,
            'member': self.member.to_dict() if self.member else None,
            'plan': self.plan.to_dict() if self.plan else None
        }

    @classmethod
    def from_dict(cls, data):
        # creates a Subscription instance from a dictionary
        member_data = data.get('member')
        plan_data = data.get('plan')
        
        member = Member.from_dict(member_data) if member_data else None
        plan = Plan.from_dict(plan_data) if plan_data else None
        
        return cls(
            id = data.get('id'),
            member_id = data.get('member_id'),
            plan_id = data.get('plan_id'),
            start_date = data.get('start_date'),
            end_date = data.get('end_date'),
            is_active = data.get('is_active', True),
            member = member,
            plan = plan
        )
    
    @classmethod
    def from_db_row(cls, row, member=None, plan=None):
        # creates a Subscription instance from a database row
        return cls(
            id = row['id'],
            member_id = row['member_id'],
            plan_id = row['plan_id'],
            start_date = row['start_date'],
            end_date = row['end_date'],
            is_active = bool(row['is_active']),
            member = member,
            plan = plan
        )

class Payment :
    def __init__(self, id = None, subscription_id = None, amount = 0.0,
                 payment_date = None, notes = "", subscription = None) :
        self.id = id
        self.subscription_id = subscription_id
        self.amount = amount
        self.payment_date = payment_date or datetime.now().date()
        self.notes = notes
        self.subscription = subscription

    def __str__(self) :
        return f"Payment #{self.id} (${self.amount})"

    def to_dict(self) :
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat() if isinstance(self.payment_date, datetime) else self.payment_date,
            'notes': self.notes,
            'subscription': self.subscription.to_dict() if self.subscription else None
        }
    
    @classmethod
    def from_dict(cls, data) :
        # create a Payment instance from a dictionary
        subscription_data = data.get('subscription')
        subscription = Subscription.from_dict(subscription_data) if subscription_data else None 

        return cls(
            id = data.get('id'),
            subscription_id = data.get('subscription_id'),
            amount = data.get('amount', 0.0),
            payment_date = data.get('payment_date'),
            notes = data.get('notes', ''),
            subscription = subscription
        )
    
    @classmethod
    def from_db_row(cls, row, subscription = None) :
        # creates a Payment instance from a database row
        return cls(
            id = row['id'],
            subscription_id = row['subscription_id'],
            amount = row['amount'],
            payment_date = row['payment_date'],
            notes = row['notes'],
            subscription = subscription
        )

        
        

