"""Database ORM models for telecom churn analytics."""

from sqlalchemy import Column, String, Integer, SmallInteger, Numeric, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(String(20), primary_key=True)
    gender = Column(String(10))
    senior_citizen = Column(SmallInteger)
    partner = Column(String(5))
    dependents = Column(String(5))
    tenure = Column(Integer, nullable=False)
    phone_service = Column(String(5))
    multiple_lines = Column(String(20))
    internet_service = Column(String(20))
    online_security = Column(String(20))
    online_backup = Column(String(20))
    device_protection = Column(String(20))
    tech_support = Column(String(20))
    streaming_tv = Column(String(20))
    streaming_movies = Column(String(20))
    contract_type = Column(String(20), index=True)
    paperless_billing = Column(String(5))
    payment_method = Column(String(30), index=True)
    monthly_charges = Column(Numeric(10, 2))
    total_charges = Column(Numeric(10, 2))
    churn = Column(Boolean, nullable=False, index=True)
    
    # Engineered features
    tenure_bucket = Column(String(20), index=True)
    spending_category = Column(String(20))
    estimated_clv = Column(Numeric(12, 2))
    age_group = Column(String(20))
    
    # Prediction results (added for Phase 4)
    churn_probability = Column(Numeric(5, 4))
    risk_tier = Column(String(10))
