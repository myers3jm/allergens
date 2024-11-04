 DROP EVENT IF EXISTS allergens_purge_menu;
 CREATE EVENT allergens_purge_menu ON SCHEDULE EVERY 1 DAY STARTS CURRENT_TIMESTAMP DO DELETE FROM menu;

-- DROP TABLE IF EXISTS menu;
-- CREATE TABLE menu(
--     product_name    VARCHAR(500) PRIMARY KEY,
--     category        TEXT NOT NULL,
--     flavor          TEXT,
--     ingredients     TEXT NOT NULL,
--     allergens       TEXT NOT NULL,
--     warning         TEXT
-- );