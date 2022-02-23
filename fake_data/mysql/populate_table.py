from concurrent.futures.process import _python_exit
from sqlalchemy import create_engine, MetaData, select
from faker import Faker
import sys
import random
import datetime
from datetime import timedelta
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
customers = metadata.tables["customer"]
staff = metadata.tables["staff"]
books = metadata.tables["book"]
authors = metadata.tables["author"]
book_author_couples = metadata.tables["book_author"]
inventories = metadata.tables["inventory"]
rentals = metadata.tables["rental"]
payments = metadata.tables["payment"]

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

        if self.table == "library":
            self.create_libraries_table()

        if self.table == "address":
            self.create_addresses_table()

        if self.table == "book":
            self.create_books_table()

        if self.table == "author":
            self.create_authors_table()

        if self.table == "staff":
            self.create_staff_table()

        if self.table == "customer":
            self.create_customers_table()

        if self.table == "book_author":
            self.create_book_author_pairs_table()

        if self.table == "inventory":
            self.create_inventories_table()

        if self.table == "rental":
            self.create_rentals_table()

        if self.table == "payment":
            self.create_payments_table()

    def create_countries_table(self):
        with engine.begin() as conn:
            for _ in range(self.num_records):
                insert_stmt = countries.insert().values(
                    country_name = faker.country_code(),
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The country table")

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
        logger.info(f"{self.num_records} was added to The city table")

    def create_addresses_table(self):
        with engine.begin() as conn:
            city_ids = conn.execute(select([cities.c.city_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = addresses.insert().values(
                    address = faker.address().replace('\n', '\\n'),
                    postal_code = faker.zipcode(),
                    phone_number = faker.phone_number(),
                    city_id = random.choice(city_ids)[0],
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to  The address table")

    def create_staff_table(self):
        with engine.begin() as conn:
            addresses_ids = conn.execute(select([addresses.c.address_id])).fetchall()
            libraries_ids = conn.execute(select([libraries.c.library_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = staff.insert().values(
                    last_name = faker.last_name(), 
                    first_name = faker.first_name(),
                    email = faker.email(),
                    address_id = random.choice(addresses_ids)[0],
                    library_id = random.choice(libraries_ids)[0],
                    active = faker.boolean(),
                    username = faker.name().replace(' ',''),
                    password = faker.password(),
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The staff table")

    def create_customers_table(self):
        with engine.begin() as conn: 
            addresses_ids = conn.execute(select([addresses.c.address_id])).fetchall()
            libraries_ids = conn.execute(select([libraries.c.library_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = customers.insert().values(
                    last_name = faker.last_name(), 
                    first_name = faker.first_name(),
                    email = faker.email(),
                    address_id = random.choice(addresses_ids)[0],
                    library_id = random.choice(libraries_ids)[0],
                    active = faker.boolean(),
                    create_date = faker.date_between(start_date = '-20y'),
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The customer table")
    
                

    def create_libraries_table(self):
        with engine.begin() as conn:
            addresses_ids = conn.execute(select([addresses.c.address_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = libraries.insert().values(
                        address_id = random.choice(addresses_ids)[0],
                        last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The library table")

    def create_books_table(self):
        with engine.begin() as conn:
            for _ in range(self.num_records):
                insert_stmt = books.insert().values(
                        title = faker.paragraph(nb_sentences=1).replace('\n', '\\n'),
                        description = faker.paragraph(nb_sentences=3).replace('\n', '\\n'),
                        release_date = faker.date_between() ,
                        language = faker.language_code(),
                        original_language = faker.language_code(),
                        rental_duration = random.randint(14, 60),
                        rating =random.randint(1,5),
                        last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The book table")

    def create_authors_table(self):
        with engine.begin() as conn: 
            for _ in range(self.num_records):
                insert_stmt = authors.insert().values(
                        first_name = faker.first_name(), 
                        last_name = faker.last_name(), 
                        last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The author table")
    
    def create_book_author_pairs_table(self): 
        with engine.begin() as conn: 
            books_ids = conn.execute(select([books.c.book_id])).fetchall()
            authors_ids = conn.execute(select([authors.c.author_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = book_author_couples.insert().values(
                    book_id = random.choice(books_ids)[0],
                    author_id = random.choice(authors_ids)[0],
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The author book couples table")


    def create_inventories_table(self): 
        with engine.begin() as conn: 
            books_ids = conn.execute(select([books.c.book_id])).fetchall()
            libraries_ids = conn.execute(select([libraries.c.library_id])).fetchall()
            for _ in range(self.num_records):
                insert_stmt = inventories.insert().values(
                    book_id = random.choice(books_ids)[0], 
                    library_id = random.choice(libraries_ids)[0], 
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The inventory table")

    def create_rentals_table(self): 
        with engine.begin() as conn:
            inventories_id_book_id_s = conn.execute(select([inventories.c.inventory_id, inventories.c.book_id])).fetchall()
            customers_id_create_date_s = conn.execute(select([customers.c.customer_id, customers.c.create_date])).fetchall()
            staff_ids = conn.execute(select([staff.c.staff_id])).fetchall()

            for _ in range(self.num_records):
                # Here I am adding some logic for the data to be a bit coherent
                inventory_id_choice, inventory_id_choice_book_id = random.choice(inventories_id_book_id_s)
                book_choice_release_date, book_choice_rental_duration = conn.execute(select([books.c.release_date,books.c.rental_duration])\
                                                                                            .where(books.c.book_id == inventory_id_choice_book_id)\
                                                                                            ).fetchone()
                customers_id_choice, customers_create_date_choice = random.choice(customers_id_create_date_s)
                # The rental date can not be before the customer account is create nor before the book was authored
                rental_date = faker.date_between(start_date = max([book_choice_release_date,customers_create_date_choice])) # by default the end date is the current
                # The return date is the rental date plus the duration of the rental of the book
                return_date = rental_date + timedelta(days = book_choice_rental_duration) 
                insert_stmt = rentals.insert().values(
                    rental_date = rental_date,
                    return_date = return_date,
                    inventory_id = inventory_id_choice, 
                    customer_id = customers_id_choice,
                    staff_id = random.choice(staff_ids)[0],
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to The rental table")

    def create_payments_table(self): 
        with engine.begin() as conn:
            rentals_ids_rental_dates_return_dates = conn.execute(select([rentals.c.rental_id,rentals.c.rental_date, rentals.c.return_date])).fetchall()
            for _ in range(self.num_records):
                rental_id_choice, rental_date_choice, return_date_choice = random.choice(rentals_ids_rental_dates_return_dates)
                insert_stmt = payments.insert().values(
                    # Here I am using a many_to_many relationship as a rental may be paid by trunks 
                    rental_id = rental_id_choice, 
                    amount = round(random.uniform(5, 25), 2),
                    # The payment date has the be between the rental date and the return date 
                    payment_date = faker.date_between(start_date = rental_date_choice,\
                            end_date =  min([datetime.datetime.now().date(),return_date_choice])) , 
                    last_update = datetime.datetime.now()
                )
                conn.execute(insert_stmt)
        logger.info(f"{self.num_records} was added to sThe payment table")

if __name__ == "__main__":
    generate_data = GenerateData()
    generate_data.create_data()
