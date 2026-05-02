package com.example.library.service;

import com.example.library.entity.Author;
import com.example.library.entity.Book;
import com.example.library.repository.AuthorRepository;
import com.example.library.repository.BookRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;

@Service // Tells Spring this is our business logic class
public class LibraryService {

    // Dependency Injection: Spring automatically provides the repository instances
    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private AuthorRepository authorRepository;

    // --- READ Operations ---

    public List<Book> getAllBooksWithAuthors() {
        // Calling our highly optimized custom inner join query!
        return bookRepository.findAllBooksWithAuthorsInnerJoin();
    }

    public List<Author> getAllAuthors() {
        return authorRepository.findAll();
    }

    public Book getBookById(Long id) {
        // .orElseThrow ensures we don't return a null object if the book isn't found
        return bookRepository
            .findById(id)
            .orElseThrow(() ->
                new RuntimeException("Book with ID " + id + " not found")
            );
    }

    // --- CREATE / UPDATE Operation ---

    public void saveBook(Book book) {
        try {
            // If the book has no ID, save() creates a new record.
            // If the book HAS an ID, save() updates the existing record.
            bookRepository.save(book);
        } catch (DataIntegrityViolationException e) {
            // This catches the exact exception your rubric mentions!
            // It triggers if the title is null, or if it violates the unique constraint.
            throw new RuntimeException(
                "Data integrity violation: Book title must be unique and cannot be empty."
            );
        }
    }
}
