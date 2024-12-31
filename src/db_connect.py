from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Float, Enum, DateTime, Date, ForeignKey, func, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pytz 
from datetime import datetime

Base = declarative_base()


class Products(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Float, default= 0.0)
    barcode = Column(String(15), unique=True, nullable=False)
    category = Column(String(100), nullable=True)
    unit = Column(String(10), nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class ProductMovements(Base):
    __tablename__ = 'product_movements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    stakeholder_id = Column(Integer, nullable=False)
    document_id = Column(Integer, nullable=False)
    movement_type = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class Stakeholders(Base):
    __tablename__ = 'stakeholders'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    type = Column(String, default='supplier')
    note = Column(String(100), nullable=True)
    debt = Column(Float, default=0.0)
    payment_date = Column(Date, default=func.now())
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class StakeholderMovements(Base):
    __tablename__ = 'stakeholder_movements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stakeholder_id = Column(Integer, nullable=False)
    document_id = Column(Integer, default=0)
    movement_type = Column(Integer, nullable=False)
    total= Column(Float, default = 0.0)
    paid= Column(Float, default = 0.0)
    debt= Column(Float, default = 0.0)
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class Documents(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    stakeholder_id = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    warhouse = Column(String(100), default = 'Əsas')
    note = Column(String(100), nullable=True)
    document_type = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))


class CheckOut(Base):
    __tablename__ = 'checkout'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    product_movement_id = Column(Integer, default=0)
    delete_status = Column(Integer, default=0)
    name = Column(String(100), nullable=False)
    barcode = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    unit = Column(String(100), nullable=False)


class CheckIn(Base):
    __tablename__ = 'checkin'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    product_movement_id = Column(Integer, default=0)
    delete_status = Column(Integer, default=0)
    name = Column(String(100), nullable=False)
    barcode = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    unit = Column(String(100), nullable=False)


class License(Base):
    __tablename__ = 'license'

    id = Column(Integer, primary_key=True)
    app_license = Column(String(100), default='no_license_key')
    created_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')))
    updated_date = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Baku')), 
                                onupdate=lambda: datetime.now(pytz.timezone('Asia/Baku')))



# Create a SQLite database
engine = create_engine('sqlite:///shop.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
