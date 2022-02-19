from sqlalchemy import create_engine, MetaData, \
    Column, Integer, Numeric, String, Boolean, DateTime, Date, Table, ForeignKey
import logging
from logging.config import fileConfig

fileConfig('./logging_conf.ini')
logger = logging.getLogger()

# Set up connection between sqlalchemy and MySql SGBD
engine = create_engine(
    "mysql+mysqlconnector://library_admin:library_admin_pass@localhost:3306/library_management"
)

# Create a metadata object
metadata = MetaData()

# DDL for customers, products, stores, and transactions
country_table = Table(
    "country",
    metadata,
    Column("country_id", Integer, primary_key=True),
    Column("country_name", String(50), nullable=False),
    Column("last_update", DateTime, nullable=False),
)
city_table = Table(
    "city",
    metadata,
    Column("city_id", Integer, primary_key=True),
    Column("country_id", ForeignKey("country.country_id"), 
            nullable=False),
    Column("city_name", String(50), nullable=False),
    Column("last_update", DateTime, nullable=False),
)
address_table = Table(
    "address", 
    metadata,
    Column("address_id", Integer, primary_key=True),
    Column("address", String(255), nullable=False),
    Column("postal_code", String(50), nullable=False),
    Column("phone_number", String(50), nullable=False),
    Column("city_id", ForeignKey("city.city_id"),
                     nullable=False),
    Column("last_update", DateTime, nullable=False),
)
library_table = Table(
    "library",
    metadata,
    Column("library_id", Integer, primary_key=True),
    Column("address_id", ForeignKey("address.address_id"),
            nullable=False),
    Column("last_update", DateTime, nullable=False),
)
staff_id = Table(
    "staff",
    metadata,
    Column("staff_id", Integer, primary_key=True),
    Column("last_name", String(50), nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("email", String(50), nullable=False),
    Column("address_id", ForeignKey("address.address_id"), 
           nullable=False),
    Column("library_id", ForeignKey("library.library_id"), 
            nullable=False),
    Column("active", Boolean, nullable=False),
    Column("username", String(50), nullable=False),
    Column("password", String(50), nullable=False),
    Column("last_update", DateTime, nullable=False)
)
customer_id = Table(
    "customer",
    metadata,
    Column("customer_id", Integer, primary_key=True),
    Column("last_name", String(50), nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("email", String(50), nullable=False),
    Column("address_id", ForeignKey("address.address_id"), 
           nullable=False),
    Column("library_id", ForeignKey("library.library_id"), 
           nullable=False),
    Column("active", Boolean, nullable=False),
    Column("create_date", DateTime, nullable=False),
    Column("last_update", DateTime, nullable=False)
)
 
# Start transaction to commit DDL to mysql database
with engine.begin() as conn:
    metadata.create_all(conn)
    # Log the tables as they are created
    for table in metadata.tables.keys():
        logger.info(f"{table} successfully created")