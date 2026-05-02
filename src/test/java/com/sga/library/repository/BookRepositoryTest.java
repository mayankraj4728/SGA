package com.sga.library.repository;

import com.sga.library.dto.BookAuthorView;
import com.sga.library.entity.Author;
import com.sga.library.entity.Book;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@AutoConfigureTestDatabase
class BookRepositoryTest {

    @Autowired
    private BookRepository bookRepository;

    @Autowired
    private AuthorRepository authorRepository;

    @Test
    void findByIsbn_returnsBookWhenPresent() {
        Author author = authorRepository.save(new Author("Test Author", "test@example.com", "British"));
        bookRepository.save(new Book("Test Book", "TEST-ISBN-001", "Fiction", 9.99, author));

        Optional<Book> found = bookRepository.findByIsbn("TEST-ISBN-001");

        assertThat(found).isPresent();
        assertThat(found.get().getTitle()).isEqualTo("Test Book");
    }

    @Test
    void findAllBooksWithAuthors_returnsInnerJoinedRows() {
        Author a1 = authorRepository.save(new Author("Alpha Author", "alpha@example.com", "American"));
        Author a2 = authorRepository.save(new Author("Beta Author", "beta@example.com", "British"));

        bookRepository.save(new Book("Alpha Book", "A-001", "Fiction", 10.0, a1));
        bookRepository.save(new Book("Beta Book", "B-001", "Mystery", 12.0, a2));

        List<BookAuthorView> rows = bookRepository.findAllBooksWithAuthors();

        assertThat(rows).hasSize(2);
        assertThat(rows).extracting(BookAuthorView::getAuthorName)
                .containsExactly("Alpha Author", "Beta Author");
        assertThat(rows).extracting(BookAuthorView::getTitle)
                .containsExactly("Alpha Book", "Beta Book");
    }

    @Test
    void findAllBooksWithAuthors_excludesAuthorsWithNoBooks() {
        Author withBook = authorRepository.save(new Author("With Book", "with@example.com", "American"));
        authorRepository.save(new Author("No Book", "no@example.com", "British"));
        bookRepository.save(new Book("Some Book", "S-001", "Fiction", 9.99, withBook));

        List<BookAuthorView> rows = bookRepository.findAllBooksWithAuthors();

        assertThat(rows).hasSize(1);
        assertThat(rows.get(0).getAuthorName()).isEqualTo("With Book");
    }
}
