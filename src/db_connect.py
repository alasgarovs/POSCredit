from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytz 
from datetime import datetime

Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100))
    product_quantity = Column(Float)
    product_buy_price = Column(Float)
    product_sale_price = Column(Float)
    product_barcode = Column(String(15), unique=True)
    date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))       
    customer_phone_1 = Column(String(20))        
    customer_phone_2 = Column(String(20))          
    customer_address = Column(String(100))     
    customer_level = Column(String(10))
    customer_debt = Column(Float, default=0.0)
    customer_payment_date = Column(Date, default=func.now())


class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    customer = Column(String(100))
    products = Column(String)
    total = Column(Float)
    paid = Column(Float)
    debt = Column(Float)
    date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    customer = Column(String(100))
    total = Column(Float)
    process = Column(Float)
    debt = Column(Float)
    status = Column(String)
    date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class CheckOut(Base):
    __tablename__ = 'checkout'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    product_name = Column(String(100))
    product_quantity = Column(Float)
    product_price = Column(Float)
    product_total_price = Column(Float)
    product_barcode = Column(String)


class License(Base):
    __tablename__ = 'license'

    id = Column(Integer, primary_key=True)
    app_license = Column(String(100), default='no_license_key')
    date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))


# Create a SQLite database
engine = create_engine('sqlite:///shop.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
