package com.example.library.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity // Tells Spring this class represents a database table
public class Author {

    @Id // Denotes the primary key
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Auto-increments the ID (1, 2, 3...)
    private Long id;

    @Column(nullable = false)
    private String name;

    // A single author can have a list of many books.
    // 'mappedBy' tells JPA that the 'author' field in the Book class owns the foreign key.
    // CascadeType.ALL means if we delete an Author, their books are also deleted.
    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
    private List<Book> books;

    // --- Constructors ---
    public Author() {}

    public Author(String name) {
        this.name = name;
    }

    // --- Getters and Setters ---
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<Book> getBooks() {
        return books;
    }

    public void setBooks(List<Book> books) {
        this.books = books;
    }
}
