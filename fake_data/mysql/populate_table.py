from sqlalchemy import create_engine, MetaData, select
from faker import Faker
import sys
import random
import datetime
import logging
from logging.config import fileConfig

# initiate the logger
fileConfig('./logging_conf.ini')
logger = logging.getLogger()

"""
Set up connection between sqlalchemy and MySql database
The URL used to connect to MySql is of the form 
mysql+mysqlconnector://<user>:<password>@<host>[:port]/<database_name>
"""
engine = create_engine(
    "mysql+mysqlconnector://library_admin:library_admin_pass@localhost:3306/library_management"
)

metadata = MetaData()
faker = Faker()

with engine.connect() as conn:
    metadata.reflect(conn)

countries = metadata.tables["country"]
cities = metadata.tables["city"]
addresses = metadata.tables["address"]
libraries = metadata.tables["library"]
staff = metadata.tables["staff"]
customers = metadata.tables["customer"]

class GenerateData:
    """
    generate a specific number of records to a target table in the
    MySql database.
    """

    def __init__(self):
        """
        define command line arguments.
        """
        self.table = sys.argv[1]
        self.num_records = int(sys.argv[2])

    def create_data(self):
        """
        using the faker library, generate data and execute DML.
        """
        if self.table not in metadata.tables.keys():
            return print(f"{self.table} does not exist")
        if self.table == "country":
            self.create_countries_table()
        if self.table == "city":
            self.create_cities_table()
        if self.table == "address":
            self.create_addresses_table()

    def create_countries_table(self):
        with engine.begin() as conn:
            for _ in range(self.num_records):
                insert_stmt = countries.insert().values(
                    country_name = faker.country_code(),
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info("The countries table is now populated with data")
    
    def create_cities_table(self):
        with engine.begin() as conn:
            country_ids = conn.execute(select([countries.c.country_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = cities.insert().values(
                    city_name = faker.city(),
                    country_id = random.choice(country_ids)[0],
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info("The cities table is now populated with data")

    def create_addresses_table(self):
        with engine.begin() as conn:
            city_ids = conn.execute(select([cities.c.city_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = addresses.insert().values(
                    address = faker.address(),
                    postal_code = faker.zipcode(),
                    phone_number = faker.phone_number(),
                    city_id = random.choice(city_ids)[0],
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info("The addresses table is now populated with data")


if __name__ == "__main__":    
    generate_data = GenerateData()   
    generate_data.create_data()