CREATE TABLE country (
    country_id SMALLINT AUTO_INCREMENT,
    country_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (country_id)
);

CREATE TABLE city (
    city_id SMALLINT AUTO_INCREMENT,
    city_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    country_id SMALLINT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id) ON DELETE CASCADE
);

CREATE TABLE address (
    address_id SMALLINT AUTO_INCREMENT,
    address VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    postal_code VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    phone_number VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    city_id SMALLINT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (address_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id) ON DELETE CASCADE
);

CREATE TABLE library (
    library_id SMALLINT AUTO_INCREMENT,
    address_id SMALLINT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (library_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE
);

CREATE TABLE staff (
    staff_id SMALLINT AUTO_INCREMENT,
    last_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    first_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    email VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    address_id SMALLINT,
    library_id SMALLINT,
    active BOOLEAN,
    username VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    password VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (staff_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE,
    FOREIGN KEY (library_id) REFERENCES library(library_id) ON DELETE CASCADE
);

CREATE TABLE customer (
    customer_id SMALLINT AUTO_INCREMENT,
    library_id SMALLINT,
    first_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    last_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    email VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    address_id SMALLINT,
    active BOOLEAN,
    create_date DATETIME,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE,
    FOREIGN KEY (library_id) REFERENCES library(library_id) ON DELETE CASCADE
);

CREATE TABLE book (
    book_id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL COLLATE 'utf8_unicode_ci',
    description TEXT,
    release_date DATE,
    language VARCHAR(20) NOT NULL COLLATE 'utf8_unicode_ci',
    original_language VARCHAR(20) NOT NULL COLLATE 'utf8_unicode_ci',
    rental_duration TINYINT,
    rating DECIMAL(3, 2),
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (book_id)
);

CREATE TABLE author (
    author_id SMALLINT AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    last_name VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci',
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (author_id)
);

CREATE TABLE book_author (
    author_id SMALLINT,
    book_id INT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES author(author_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE
);

CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT,
    book_id INT,
    library_id SMALLINT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (inventory_id),
    FOREIGN KEY (library_id) REFERENCES library (library_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE
);

CREATE TABLE rental (
    rental_id INT AUTO_INCREMENT,
    rental_date DATETIME,
    inventory_id INT,
    customer_id SMALLINT,
    return_date DATETIME,
    staff_id SMALLINT,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rental_id),
    FOREIGN KEY (inventory_id) REFERENCES inventory(inventory_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
);

CREATE TABLE payment (
    payment_id SMALLINT AUTO_INCREMENT,
    rental_id INT,
    amount DECIMAL(5, 2),
    payment_date DATETIME,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (payment_id),
    FOREIGN KEY (rental_id) REFERENCES rental(rental_id) ON DELETE CASCADE
);