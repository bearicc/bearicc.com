CREATE TABLE IF NOT EXISTS bearicc.blog (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    author VARCHAR(128) NOT NULL,
    source_file VARCHAR(128) DEFAULT '',
    content TEXT DEFAULT '',
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
