package com.sga.library.service;

import com.sga.library.entity.Author;
import com.sga.library.exception.ResourceNotFoundException;
import com.sga.library.repository.AuthorRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class AuthorService {

    private final AuthorRepository authorRepository;

    public AuthorService(AuthorRepository authorRepository) {
        this.authorRepository = authorRepository;
    }

    @Transactional(readOnly = true)
    public List<Author> findAll() {
        return authorRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Author findById(Long id) {
        return authorRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Author not found with id " + id));
    }

    public Author create(Author author) {
        try {
            return authorRepository.save(author);
        } catch (DataIntegrityViolationException ex) {
            throw new DataIntegrityViolationException(
                    "Could not save author: an author with email '" + author.getEmail() + "' already exists.", ex);
        }
    }

    public Author update(Long id, Author updated) {
        Author existing = findById(id);
        existing.setName(updated.getName());
        existing.setEmail(updated.getEmail());
        existing.setNationality(updated.getNationality());
        try {
            return authorRepository.save(existing);
        } catch (DataIntegrityViolationException ex) {
            throw new DataIntegrityViolationException(
                    "Could not update author: email '" + updated.getEmail() + "' is already used by another author.", ex);
        }
    }
}
