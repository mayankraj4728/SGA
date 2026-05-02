package com.sga.library.service;

import com.sga.library.dto.BookAuthorView;
import com.sga.library.entity.Author;
import com.sga.library.entity.Book;
import com.sga.library.exception.ResourceNotFoundException;
import com.sga.library.repository.BookRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class BookService {

    private final BookRepository bookRepository;
    private final AuthorService authorService;

    public BookService(BookRepository bookRepository, AuthorService authorService) {
        this.bookRepository = bookRepository;
        this.authorService = authorService;
    }

    @Transactional(readOnly = true)
    public List<Book> findAll() {
        return bookRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Book findById(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id " + id));
    }

    @Transactional(readOnly = true)
    public List<BookAuthorView> findAllBooksWithAuthors() {
        return bookRepository.findAllBooksWithAuthors();
    }

    public Book create(Book book, Long authorId) {
        Author author = authorService.findById(authorId);
        book.setAuthor(author);
        try {
            return bookRepository.save(book);
        } catch (DataIntegrityViolationException ex) {
            throw new DataIntegrityViolationException(
                    "Could not save book: a book with ISBN '" + book.getIsbn() + "' already exists.", ex);
        }
    }

    public Book update(Long id, Book updated, Long authorId) {
        Book existing = findById(id);
        existing.setTitle(updated.getTitle());
        existing.setIsbn(updated.getIsbn());
        existing.setGenre(updated.getGenre());
        existing.setPrice(updated.getPrice());
        if (authorId != null) {
            existing.setAuthor(authorService.findById(authorId));
        }
        try {
            return bookRepository.save(existing);
        } catch (DataIntegrityViolationException ex) {
            throw new DataIntegrityViolationException(
                    "Could not update book: ISBN '" + updated.getIsbn() + "' is already used by another book.", ex);
        }
    }
}
