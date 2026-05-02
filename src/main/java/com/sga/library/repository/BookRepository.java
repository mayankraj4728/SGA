package com.sga.library.repository;

import com.sga.library.dto.BookAuthorView;
import com.sga.library.entity.Book;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BookRepository extends JpaRepository<Book, Long> {

    Optional<Book> findByIsbn(String isbn);

    /**
     * Custom JPQL query performing an INNER JOIN between Book and Author,
     * projecting the joined columns into BookAuthorView.
     */
    @Query("""
            SELECT new com.sga.library.dto.BookAuthorView(
                b.id, b.title, b.isbn, b.genre, b.price,
                a.id, a.name, a.email, a.nationality)
            FROM Book b
            INNER JOIN b.author a
            ORDER BY a.name ASC, b.title ASC
            """)
    List<BookAuthorView> findAllBooksWithAuthors();
}
