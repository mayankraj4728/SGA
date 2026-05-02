package com.sga.library.service;

import com.sga.library.dto.BookAuthorView;
import com.sga.library.entity.Author;
import com.sga.library.entity.Book;
import com.sga.library.exception.ResourceNotFoundException;
import com.sga.library.repository.BookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataIntegrityViolationException;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @Mock
    private AuthorService authorService;

    @InjectMocks
    private BookService bookService;

    private Author author;
    private Book book;

    @BeforeEach
    void setUp() {
        author = new Author("Author", "author@example.com", "American");
        author.setId(10L);
        book = new Book("Title", "ISBN-1", "Fiction", 9.99, author);
        book.setId(1L);
    }

    @Test
    void findById_throwsWhenMissing() {
        when(bookRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> bookService.findById(99L))
                .isInstanceOf(ResourceNotFoundException.class);
    }

    @Test
    void create_attachesAuthorAndSaves() {
        when(authorService.findById(10L)).thenReturn(author);
        when(bookRepository.save(any(Book.class))).thenAnswer(inv -> {
            Book b = inv.getArgument(0);
            b.setId(1L);
            return b;
        });

        Book input = new Book("Title", "ISBN-1", "Fiction", 9.99, null);
        Book result = bookService.create(input, 10L);

        assertThat(result.getAuthor()).isEqualTo(author);
        assertThat(result.getId()).isEqualTo(1L);
    }

    @Test
    void create_translatesIntegrityViolation() {
        when(authorService.findById(10L)).thenReturn(author);
        when(bookRepository.save(any(Book.class)))
                .thenThrow(new DataIntegrityViolationException("dup"));

        Book input = new Book("Dup", "ISBN-DUP", "Fiction", 9.99, null);

        assertThatThrownBy(() -> bookService.create(input, 10L))
                .isInstanceOf(DataIntegrityViolationException.class)
                .hasMessageContaining("ISBN-DUP");
    }

    @Test
    void update_appliesChangesAndPersists() {
        when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
        when(authorService.findById(10L)).thenReturn(author);
        when(bookRepository.save(any(Book.class))).thenAnswer(inv -> inv.getArgument(0));

        Book updated = new Book("New Title", "ISBN-2", "Mystery", 14.50, null);
        Book result = bookService.update(1L, updated, 10L);

        assertThat(result.getTitle()).isEqualTo("New Title");
        assertThat(result.getIsbn()).isEqualTo("ISBN-2");
        assertThat(result.getGenre()).isEqualTo("Mystery");
        assertThat(result.getPrice()).isEqualTo(14.50);
        assertThat(result.getAuthor()).isEqualTo(author);
    }

    @Test
    void findAllBooksWithAuthors_returnsRepositoryRows() {
        BookAuthorView row = new BookAuthorView(1L, "T", "I", "G", 9.99, 10L, "A", "e@e.com", "USA");
        when(bookRepository.findAllBooksWithAuthors()).thenReturn(List.of(row));

        List<BookAuthorView> rows = bookService.findAllBooksWithAuthors();

        assertThat(rows).hasSize(1);
        assertThat(rows.get(0).getAuthorName()).isEqualTo("A");
    }
}
