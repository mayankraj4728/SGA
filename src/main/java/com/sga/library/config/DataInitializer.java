package com.sga.library.config;

import com.sga.library.entity.Author;
import com.sga.library.entity.Book;
import com.sga.library.repository.AuthorRepository;
import com.sga.library.repository.BookRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner seedDatabase(AuthorRepository authorRepository, BookRepository bookRepository) {
        return args -> {
            if (authorRepository.count() > 0) {
                return;
            }

            List<Author> authors = List.of(
                    new Author("George Orwell", "george.orwell@example.com", "British"),
                    new Author("Jane Austen", "jane.austen@example.com", "British"),
                    new Author("Mark Twain", "mark.twain@example.com", "American"),
                    new Author("Leo Tolstoy", "leo.tolstoy@example.com", "Russian"),
                    new Author("Gabriel Garcia Marquez", "gabriel.gm@example.com", "Colombian"),
                    new Author("Haruki Murakami", "haruki.murakami@example.com", "Japanese"),
                    new Author("Chimamanda Ngozi Adichie", "chimamanda.na@example.com", "Nigerian"),
                    new Author("J.K. Rowling", "jk.rowling@example.com", "British"),
                    new Author("Ernest Hemingway", "ernest.h@example.com", "American"),
                    new Author("Agatha Christie", "agatha.c@example.com", "British")
            );
            authorRepository.saveAll(authors);

            List<Book> books = List.of(
                    new Book("1984", "978-0451524935", "Dystopian", 14.99, authors.get(0)),
                    new Book("Pride and Prejudice", "978-1503290563", "Romance", 9.99, authors.get(1)),
                    new Book("The Adventures of Huckleberry Finn", "978-0486280615", "Adventure", 7.50, authors.get(2)),
                    new Book("War and Peace", "978-1400079988", "Historical", 19.99, authors.get(3)),
                    new Book("One Hundred Years of Solitude", "978-0060883287", "Magical Realism", 16.49, authors.get(4)),
                    new Book("Norwegian Wood", "978-0375704024", "Fiction", 13.50, authors.get(5)),
                    new Book("Half of a Yellow Sun", "978-1400095209", "Historical", 15.25, authors.get(6)),
                    new Book("Harry Potter and the Sorcerer's Stone", "978-0590353427", "Fantasy", 12.99, authors.get(7)),
                    new Book("The Old Man and the Sea", "978-0684801223", "Fiction", 10.75, authors.get(8)),
                    new Book("Murder on the Orient Express", "978-0062693662", "Mystery", 11.99, authors.get(9))
            );
            bookRepository.saveAll(books);
        };
    }
}
