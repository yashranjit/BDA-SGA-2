-- Insert 10 Authors
INSERT INTO author (name) VALUES ('George Orwell');
INSERT INTO author (name) VALUES ('J.K. Rowling');
INSERT INTO author (name) VALUES ('J.R.R. Tolkien');
INSERT INTO author (name) VALUES ('Agatha Christie');
INSERT INTO author (name) VALUES ('Stephen King');
INSERT INTO author (name) VALUES ('Isaac Asimov');
INSERT INTO author (name) VALUES ('Jane Austen');
INSERT INTO author (name) VALUES ('F. Scott Fitzgerald');
INSERT INTO author (name) VALUES ('Arthur Conan Doyle');
INSERT INTO author (name) VALUES ('Mary Shelley');

-- Insert 10 Books (Notice how the author_id maps to the IDs 1-10 generated above)
INSERT INTO book (title, genre, author_id) VALUES ('1984', 'Dystopian', 1);
INSERT INTO book (title, genre, author_id) VALUES ('Harry Potter and the Sorcerer''s Stone', 'Fantasy', 2);
INSERT INTO book (title, genre, author_id) VALUES ('The Fellowship of the Ring', 'High Fantasy', 3);
INSERT INTO book (title, genre, author_id) VALUES ('Murder on the Orient Express', 'Mystery', 4);
INSERT INTO book (title, genre, author_id) VALUES ('The Shining', 'Horror', 5);
INSERT INTO book (title, genre, author_id) VALUES ('Foundation', 'Science Fiction', 6);
INSERT INTO book (title, genre, author_id) VALUES ('Pride and Prejudice', 'Romance', 7);
INSERT INTO book (title, genre, author_id) VALUES ('The Great Gatsby', 'Tragedy', 8);
INSERT INTO book (title, genre, author_id) VALUES ('The Hound of the Baskervilles', 'Detective Fiction', 9);
INSERT INTO book (title, genre, author_id) VALUES ('Frankenstein', 'Gothic Science Fiction', 10);
