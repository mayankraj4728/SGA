package com.sga.library.controller;

import com.sga.library.entity.Author;
import com.sga.library.service.AuthorService;
import jakarta.validation.Valid;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/authors")
public class AuthorController {

    private final AuthorService authorService;

    public AuthorController(AuthorService authorService) {
        this.authorService = authorService;
    }

    @GetMapping
    public String list(Model model) {
        model.addAttribute("authors", authorService.findAll());
        return "authors/list";
    }

    @GetMapping("/new")
    public String createForm(Model model) {
        model.addAttribute("author", new Author());
        return "authors/form";
    }

    @PostMapping
    public String create(@Valid @ModelAttribute("author") Author author,
                         BindingResult result,
                         Model model,
                         RedirectAttributes redirectAttrs) {
        if (result.hasErrors()) {
            return "authors/form";
        }
        try {
            authorService.create(author);
            redirectAttrs.addFlashAttribute("message", "Author created successfully.");
            return "redirect:/authors";
        } catch (DataIntegrityViolationException ex) {
            model.addAttribute("error", ex.getMessage());
            return "authors/form";
        }
    }

    @GetMapping("/{id}/edit")
    public String editForm(@PathVariable Long id, Model model) {
        model.addAttribute("author", authorService.findById(id));
        return "authors/edit";
    }

    @PostMapping("/{id}")
    public String update(@PathVariable Long id,
                         @Valid @ModelAttribute("author") Author author,
                         BindingResult result,
                         Model model,
                         RedirectAttributes redirectAttrs) {
        if (result.hasErrors()) {
            return "authors/edit";
        }
        try {
            authorService.update(id, author);
            redirectAttrs.addFlashAttribute("message", "Author updated successfully.");
            return "redirect:/authors";
        } catch (DataIntegrityViolationException ex) {
            model.addAttribute("error", ex.getMessage());
            return "authors/edit";
        }
    }
}
