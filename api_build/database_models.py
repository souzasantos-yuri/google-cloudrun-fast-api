from sqlalchemy import Column, Date, String, Integer, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    cd_customer = Column(String(256), primary_key=True)
    nm_customer = Column(String(135))
    st_email = Column(String(135))
    st_phone = Column(String(135))
    st_state = Column(String(2))
    dt_birth = Column(Date)
    orders = relationship("Order", back_populates="customer")

class Order(Base):

    __tablename__ = 'orders'
    cd_order = Column(String(256), primary_key=True)
    cd_customer = Column(
        String(256),
        ForeignKey("customers.cd_customer"),
        nullable=False
    )

    dt_order = Column(Date, nullable=False)
    nm_product = Column(String(256), nullable=False)
    qt_item = Column(Integer, nullable=False)
    vl_price = Column(Numeric, nullable=False)
    vl_shipping = Column(Numeric, nullable=False)
    vl_total = Column(Numeric, nullable=False)
    customer = relationship("Customer", back_populates="orders")