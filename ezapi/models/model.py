from pqb import Column

class Branch(object):
    '''A model representing the branches table in db'''
    __tablename__ = 'branches'

    id = Column('id')
    name = Column('name')
    address = Column('address')
    branch_code = Column('branch_code')
    remarks = Column('remarks')
    created_at = Column('created_at')
    updated_at = Column('updated_at')
    verified = Column('verified')

class Denomination(object):
    __tablename__ = 'denominations'

    id = Column('id')
    denomination_unit = Column('denomination_unit')
    remarks = Column('remarks')

class Deposit(object):
    __tablename__ = 'deposits'

    id = Column('id')
    cvs_tranid = Column('cvs_tranid')
    transaction_approved = Column('transaction_approved')
    teller_cash_account = Column('teller_cash_account')
    created_at = Column('created_at')
    updated_at = Column('updated_at')
    transaction_timestamp = Column('transaction_timestamp') #this must be modified in database
    deposit_amount = Column('deposit_amount')
    customer_name = Column('customer_name')
    deposit_account_num = Column('deposit_account_num')
    branch_id = Column('branch_id')
    teller_id = Column('teller_id')

class Role(object):
    __tablename__ = 'roles'

    id = Column('id')
    role_type = Column('role_type')
    created_at = Column('created_at')
    updated_at = Column('updated_at')

class Teller(object):
    __tablename__ = 'tellers'
    
    id = Column('id')
    teller_id = Column('teller_id')
    password = Column('password')
    created_at = Column('created_at')
    updated_at = Column('updated_at')
    access_token = Column('access_token')
    expiry_date = Column('expiry_date')
    verified = Column('verified')
    activate = Column('activate')
    teller_cash_account = Column('teller_cash_account')
    branch_id = Column('branch_id')

