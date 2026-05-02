package com.example.library.entity;

import jakarta.persistence.*;

@Entity
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Enforcing data integrity: titles cannot be null and must be unique
    @Column(nullable = false, unique = true)
    private String title;

    private String genre;

    // Many books can belong to one author.
    // @JoinColumn specifies the actual foreign key column name in the database.
    @ManyToOne
    @JoinColumn(name = "author_id", nullable = false)
    private Author author;

    // --- Constructors ---
    public Book() {}

    public Book(String title, String genre, Author author) {
        this.title = title;
        this.genre = genre;
        this.author = author;
    }

    // --- Getters and Setters ---
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public Author getAuthor() {
        return author;
    }

    public void setAuthor(Author author) {
        this.author = author;
    }
}
