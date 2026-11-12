CREATE TABLE IF NOT EXISTS brews (
    id SERIAL PRIMARY KEY,
    bean_name VARCHAR(100) NOT NULL,
    method VARCHAR(50) NOT NULL,
    grind_size VARCHAR(50),
    rating INT,
    notes TEXT
);