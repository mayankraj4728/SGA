package com.sga.library.dto;

public class BookAuthorView {
    private final Long bookId;
    private final String title;
    private final String isbn;
    private final String genre;
    private final Double price;
    private final Long authorId;
    private final String authorName;
    private final String authorEmail;
    private final String authorNationality;

    public BookAuthorView(Long bookId, String title, String isbn, String genre, Double price,
                          Long authorId, String authorName, String authorEmail, String authorNationality) {
        this.bookId = bookId;
        this.title = title;
        this.isbn = isbn;
        this.genre = genre;
        this.price = price;
        this.authorId = authorId;
        this.authorName = authorName;
        this.authorEmail = authorEmail;
        this.authorNationality = authorNationality;
    }

    public Long getBookId() { return bookId; }
    public String getTitle() { return title; }
    public String getIsbn() { return isbn; }
    public String getGenre() { return genre; }
    public Double getPrice() { return price; }
    public Long getAuthorId() { return authorId; }
    public String getAuthorName() { return authorName; }
    public String getAuthorEmail() { return authorEmail; }
    public String getAuthorNationality() { return authorNationality; }
}
