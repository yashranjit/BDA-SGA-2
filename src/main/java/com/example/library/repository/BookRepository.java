package com.example.library.repository;

import com.example.library.entity.Book;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface BookRepository extends JpaRepository<Book, Long> {
    // CUSTOM QUERY: Fulfills the "inner join" requirement
    // JPQL (Java Persistence Query Language) uses our Java class names, not table names.
    // "FETCH" tells Hibernate to grab the author data in the same single query.
    @Query("SELECT b FROM Book b INNER JOIN FETCH b.author")
    List<Book> findAllBooksWithAuthorsInnerJoin();
}
