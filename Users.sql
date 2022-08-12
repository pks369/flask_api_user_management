CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY  ,
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    pic_url varchar(255) NOT NULL,
    mobile varchar(255) NOT NULL UNIQUE
);


CREATE TABLE Address (
    add_id SERIAL PRIMARY KEY ,
	u_id int NOT NULL UNIQUE,
    house_no varchar(255) NOT NULL,
    address_line_1 varchar(255) ,
    address_line_2 varchar(255),
    city varchar(255) NOT NULL,
    stat  varchar(255) NOT NULL,
	pin_code  varchar(255) NOT NULL
);