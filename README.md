# SGA Library Management — Spring Boot CRUD

Spring Boot application managing **Authors** and **Books** with a One-to-Many relationship. Supports Create, Read, Update via JSP views and includes a custom inner-join query.

## Stack

- Spring Boot 3.2.5 (Java 17)
- Spring Data JPA + Hibernate
- H2 in-memory database
- JSP + JSTL views, custom CSS
- JUnit 5 + Mockito tests

## Domain Model

```
Author (1) ───< (N) Book
```

| Author       | Book                |
|--------------|---------------------|
| id           | id                  |
| name         | title               |
| email (uniq) | isbn (uniq)         |
| nationality  | genre               |
|              | price               |
|              | author_id (FK)      |

The relationship is mapped with `@OneToMany(mappedBy="author")` on `Author` and `@ManyToOne` on `Book`.

## Run

```bash
mvn spring-boot:run
```

Then open:

- `http://localhost:8080/` — home
- `http://localhost:8080/authors` — author list / create / edit
- `http://localhost:8080/books` — book list / create / edit
- `http://localhost:8080/books/with-authors` — custom **inner-join** report
- `http://localhost:8080/h2-console` — DB console (JDBC URL: `jdbc:h2:mem:librarydb`)

10 authors and 10 books are seeded on first start by `DataInitializer`.

## Project Layout

```
src/main/java/com/sga/library/
├── LibraryApplication.java      # Spring Boot entrypoint
├── entity/                      # JPA entities (Author, Book)
├── repository/                  # JpaRepository interfaces + custom query
├── service/                     # Business logic + integrity-violation handling
├── controller/                  # Spring MVC controllers + GlobalExceptionHandler
├── dto/                         # BookAuthorView projection for the join query
├── exception/                   # ResourceNotFoundException
└── config/                      # DataInitializer (seed data)

src/main/webapp/WEB-INF/views/   # JSPs (list / form / edit / with-authors)
src/main/resources/static/css/   # styles.css
src/test/java/com/sga/library/   # Repository (DataJpaTest) and service (Mockito) tests
```

## Custom Inner-Join Query

`BookRepository.findAllBooksWithAuthors()`:

```java
@Query("""
    SELECT new com.sga.library.dto.BookAuthorView(
        b.id, b.title, b.isbn, b.genre, b.price,
        a.id, a.name, a.email, a.nationality)
    FROM Book b
    INNER JOIN b.author a
    ORDER BY a.name ASC, b.title ASC
    """)
List<BookAuthorView> findAllBooksWithAuthors();
```

The result is rendered at `/books/with-authors`.

## Testing

```bash
mvn test
```

- `AuthorRepositoryTest`, `BookRepositoryTest` — `@DataJpaTest` against H2; verifies the custom inner-join query and unique-email integrity.
- `AuthorServiceTest`, `BookServiceTest` — Mockito unit tests for service logic, including translation of `DataIntegrityViolationException`.

## Exception Handling

- `ResourceNotFoundException` → 404
- `DataIntegrityViolationException` (e.g., duplicate ISBN/email) is caught in services and re-thrown with a user-friendly message; controllers re-render the form with an inline error.
- Uncaught exceptions are routed by `GlobalExceptionHandler` to `error.jsp`.
