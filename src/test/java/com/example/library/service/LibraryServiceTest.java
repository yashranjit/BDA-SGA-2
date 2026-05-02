package com.example.library.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.example.library.entity.Author;
import com.example.library.entity.Book;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class LibraryServiceTest {

    @Autowired
    private LibraryService libraryService;

    @Test
    void getAllBooksWithAuthorsReturnsSeededBooks() {
        List<Book> books = libraryService.getAllBooksWithAuthors();

        assertFalse(books.isEmpty());
        assertTrue(
            books.stream().anyMatch(book -> "1984".equals(book.getTitle()))
        );
        assertTrue(books.stream().allMatch(book -> book.getAuthor() != null));
    }

    @Test
    void getBookByIdReturnsSeededBook() {
        Book book = libraryService.getBookById(1L);

        assertEquals("1984", book.getTitle());
        assertNotNull(book.getAuthor());
        assertEquals("George Orwell", book.getAuthor().getName());
    }

    @Test
    void saveBookThrowsFriendlyMessageOnIntegrityViolation() {
        Author author = libraryService.getAllAuthors().get(0);
        Book duplicate = new Book("1984", "Dystopian", author);

        RuntimeException exception = assertThrows(
            RuntimeException.class,
            () -> libraryService.saveBook(duplicate)
        );

        assertEquals(
            "Data integrity violation: Book title must be unique and cannot be empty.",
            exception.getMessage()
        );
    }
}
