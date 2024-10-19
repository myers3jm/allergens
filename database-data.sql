DROP TABLE IF EXISTS menu;
CREATE TABLE menu(
    product_name    varchar(50) PRIMARY KEY,
    category    varchar(100) NOT NULL,
    flavor        varchar(50) NOT NULL,
    ingredients       varchar(50) NOT NULL,
    allergens   varchar(50) NOT NULL
);
INSERT INTO menu (product_name, category, flavor, ingredients, allergens) VALUES ('Butter Pecan Cold Brew with Sweet Cold Foam', 'Cold Brew Coffee', 'Butter Pecan', 'Lots of stuff', 'Milk, Soy');