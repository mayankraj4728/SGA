package com.sga.library.service;

import com.sga.library.entity.Author;
import com.sga.library.exception.ResourceNotFoundException;
import com.sga.library.repository.AuthorRepository;
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
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthorServiceTest {

    @Mock
    private AuthorRepository authorRepository;

    @InjectMocks
    private AuthorService authorService;

    private Author sample;

    @BeforeEach
    void setUp() {
        sample = new Author("Sample", "sample@example.com", "American");
        sample.setId(1L);
    }

    @Test
    void findAll_delegatesToRepository() {
        when(authorRepository.findAll()).thenReturn(List.of(sample));

        List<Author> result = authorService.findAll();

        assertThat(result).hasSize(1).containsExactly(sample);
        verify(authorRepository).findAll();
    }

    @Test
    void findById_returnsAuthorWhenPresent() {
        when(authorRepository.findById(1L)).thenReturn(Optional.of(sample));

        Author result = authorService.findById(1L);

        assertThat(result.getName()).isEqualTo("Sample");
    }

    @Test
    void findById_throwsWhenMissing() {
        when(authorRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> authorService.findById(99L))
                .isInstanceOf(ResourceNotFoundException.class);
    }

    @Test
    void create_savesAuthor() {
        when(authorRepository.save(any(Author.class))).thenReturn(sample);

        Author result = authorService.create(new Author("Sample", "sample@example.com", "American"));

        assertThat(result.getId()).isEqualTo(1L);
        verify(authorRepository).save(any(Author.class));
    }

    @Test
    void create_translatesIntegrityViolation() {
        when(authorRepository.save(any(Author.class)))
                .thenThrow(new DataIntegrityViolationException("constraint"));

        Author dup = new Author("X", "dup@example.com", "Y");

        assertThatThrownBy(() -> authorService.create(dup))
                .isInstanceOf(DataIntegrityViolationException.class)
                .hasMessageContaining("dup@example.com");
    }

    @Test
    void update_appliesChangesAndSaves() {
        when(authorRepository.findById(1L)).thenReturn(Optional.of(sample));
        when(authorRepository.save(any(Author.class))).thenAnswer(inv -> inv.getArgument(0));

        Author updated = new Author("Updated", "updated@example.com", "Canadian");
        Author result = authorService.update(1L, updated);

        assertThat(result.getName()).isEqualTo("Updated");
        assertThat(result.getEmail()).isEqualTo("updated@example.com");
        assertThat(result.getNationality()).isEqualTo("Canadian");
    }
}
