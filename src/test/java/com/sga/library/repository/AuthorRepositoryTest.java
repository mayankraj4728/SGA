package com.sga.library.repository;

import com.sga.library.entity.Author;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.dao.DataIntegrityViolationException;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@DataJpaTest
@AutoConfigureTestDatabase
class AuthorRepositoryTest {

    @Autowired
    private AuthorRepository authorRepository;

    @Test
    void findByEmail_returnsAuthorWhenPresent() {
        authorRepository.save(new Author("Find Me", "findme@example.com", "American"));

        Optional<Author> found = authorRepository.findByEmail("findme@example.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Find Me");
    }

    @Test
    void duplicateEmail_throwsDataIntegrityViolation() {
        authorRepository.saveAndFlush(new Author("First", "dup@example.com", "American"));
        Author second = new Author("Second", "dup@example.com", "British");

        assertThatThrownBy(() -> authorRepository.saveAndFlush(second))
                .isInstanceOf(DataIntegrityViolationException.class);
    }
}
