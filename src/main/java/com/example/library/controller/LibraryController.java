package com.example.library.controller;

import com.example.library.entity.Book;
import com.example.library.service.LibraryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller // Tells Spring this class handles web requests and returns views (JSPs)
@RequestMapping("/books") // Base URL for all methods in this controller
public class LibraryController {

    @Autowired
    private LibraryService libraryService;

    // --- READ Operation ---
    // Maps to GET requests at "/books"
    @GetMapping
    public String listBooks(Model model) {
        // Fetch all books (with authors) and add them to the Model.
        // The Model is how we pass data from Java to the JSP file.
        model.addAttribute("books", libraryService.getAllBooksWithAuthors());

        // Returns the name of the JSP file to render (list-books.jsp)
        return "list-books";
    }

    // --- CREATE Operation (Show Form) ---
    // Maps to GET requests at "/books/new"
    @GetMapping("/new")
    public String showAddForm(Model model) {
        // We pass an empty Book object to the form so the JSP can bind inputs to it
        model.addAttribute("book", new Book());
        // We also need the list of authors so the user can select one from a dropdown
        model.addAttribute("authors", libraryService.getAllAuthors());

        return "book-form"; // Returns book-form.jsp
    }

    // --- CREATE / UPDATE Operation (Process Form) ---
    // Maps to POST requests at "/books/save"
    @PostMapping("/save")
    public String saveBook(
        @ModelAttribute("book") Book book,
        RedirectAttributes redirectAttributes
    ) {
        try {
            // Send the data to the Service layer to be saved
            libraryService.saveBook(book);
            // Flash attributes survive a redirect, perfect for success messages
            redirectAttributes.addFlashAttribute(
                "success",
                "Book saved successfully!"
            );
        } catch (RuntimeException e) {
            // If the Service layer throws our DataIntegrityViolationException, catch it here
            redirectAttributes.addFlashAttribute("error", e.getMessage());
            // Send them back to the form if there was an error
            return "redirect:/books/new";
        }

        // If successful, redirect back to the main list
        return "redirect:/books";
    }

    // --- UPDATE Operation (Show Form with Data) ---
    // Maps to GET requests at "/books/edit/{id}"
    @GetMapping("/edit/{id}")
    public String showEditForm(@PathVariable Long id, Model model) {
        // Fetch the existing book by its ID
        model.addAttribute("book", libraryService.getBookById(id));
        // Fetch authors for the dropdown
        model.addAttribute("authors", libraryService.getAllAuthors());

        // Notice we reuse the exact same form used for creating!
        return "book-form";
    }
}
