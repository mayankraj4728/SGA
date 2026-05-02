package com.sga.library.controller;

import com.sga.library.entity.Book;
import com.sga.library.service.AuthorService;
import com.sga.library.service.BookService;
import jakarta.validation.Valid;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/books")
public class BookController {

    private final BookService bookService;
    private final AuthorService authorService;

    public BookController(BookService bookService, AuthorService authorService) {
        this.bookService = bookService;
        this.authorService = authorService;
    }

    @GetMapping
    public String list(Model model) {
        model.addAttribute("books", bookService.findAll());
        return "books/list";
    }

    @GetMapping("/with-authors")
    public String listWithAuthors(Model model) {
        model.addAttribute("rows", bookService.findAllBooksWithAuthors());
        return "books/with-authors";
    }

    @GetMapping("/new")
    public String createForm(Model model) {
        model.addAttribute("book", new Book());
        model.addAttribute("authors", authorService.findAll());
        return "books/form";
    }

    @PostMapping
    public String create(@Valid @ModelAttribute("book") Book book,
                         BindingResult result,
                         @RequestParam("authorId") Long authorId,
                         Model model,
                         RedirectAttributes redirectAttrs) {
        if (result.hasErrors()) {
            model.addAttribute("authors", authorService.findAll());
            return "books/form";
        }
        try {
            bookService.create(book, authorId);
            redirectAttrs.addFlashAttribute("message", "Book created successfully.");
            return "redirect:/books";
        } catch (DataIntegrityViolationException ex) {
            model.addAttribute("authors", authorService.findAll());
            model.addAttribute("error", ex.getMessage());
            return "books/form";
        }
    }

    @GetMapping("/{id}/edit")
    public String editForm(@PathVariable Long id, Model model) {
        model.addAttribute("book", bookService.findById(id));
        model.addAttribute("authors", authorService.findAll());
        return "books/edit";
    }

    @PostMapping("/{id}")
    public String update(@PathVariable Long id,
                         @Valid @ModelAttribute("book") Book book,
                         BindingResult result,
                         @RequestParam("authorId") Long authorId,
                         Model model,
                         RedirectAttributes redirectAttrs) {
        if (result.hasErrors()) {
            model.addAttribute("authors", authorService.findAll());
            return "books/edit";
        }
        try {
            bookService.update(id, book, authorId);
            redirectAttrs.addFlashAttribute("message", "Book updated successfully.");
            return "redirect:/books";
        } catch (DataIntegrityViolationException ex) {
            model.addAttribute("authors", authorService.findAll());
            model.addAttribute("error", ex.getMessage());
            return "books/edit";
        }
    }
}
