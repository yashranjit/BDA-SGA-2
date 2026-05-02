from pathlib import Path
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "documentation"
SHOT_DIR = OUT_DIR / "screenshots"
PDF_PATH = OUT_DIR / "Library_Project_Report.pdf"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#172033"),
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=28,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontSize=10.2,
        leading=14.2,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Caption",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=8.7,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        spaceBefore=3,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="TableHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11,
        textColor=colors.white,
    )
)
styles.add(
    ParagraphStyle(
        name="TableCell",
        parent=styles["Normal"],
        fontSize=8.8,
        leading=11,
        textColor=colors.HexColor("#111827"),
    )
)
styles.add(
    ParagraphStyle(
        name="CodeLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.8,
        leading=11,
        textColor=colors.HexColor("#334155"),
        spaceBefore=4,
        spaceAfter=2,
    )
)


def p(text, style="Body"):
    return Paragraph(text, styles[style])


def bullets(items):
    return ListFlowable(
        [ListItem(p(item), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=18,
        bulletFontSize=7,
        spaceAfter=8,
    )


def code_block(label, code):
    wrapped_lines = []
    for line in textwrap.dedent(code).strip("\n").splitlines():
        if len(line) <= 92:
            wrapped_lines.append(line)
            continue
        indent = len(line) - len(line.lstrip())
        wrapped = textwrap.wrap(
            line,
            width=92,
            subsequent_indent=" " * (indent + 4),
            break_long_words=False,
            break_on_hyphens=False,
        )
        wrapped_lines.extend(wrapped or [""])
    return KeepTogether(
        [
            p(label, "CodeLabel"),
            Table(
                [
                    [
                        Preformatted(
                            "\n".join(wrapped_lines),
                            ParagraphStyle(
                                "Code",
                                fontName="Courier",
                                fontSize=7.4,
                                leading=9.2,
                                textColor=colors.HexColor("#111827"),
                            ),
                        )
                    ]
                ],
                colWidths=[6.55 * inch],
                style=[
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#cbd5e1")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ],
            ),
            Spacer(1, 8),
        ]
    )


def screenshot(name, caption):
    path = SHOT_DIR / name
    img = Image(str(path))
    max_w = 6.55 * inch
    max_h = 3.9 * inch
    ratio = min(max_w / img.drawWidth, max_h / img.drawHeight)
    img.drawWidth *= ratio
    img.drawHeight *= ratio
    return KeepTogether([img, p(caption, "Caption")])


class ERDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 6.55 * inch
        self.height = 2.75 * inch

    def wrap(self, avail_width, avail_height):
        return self.width, self.height

    def draw_table(self, c, x, y, w, title, rows):
        header_h = 24
        row_h = 20
        h = header_h + row_h * len(rows)
        c.setStrokeColor(colors.HexColor("#334155"))
        c.setLineWidth(0.9)
        c.setFillColor(colors.HexColor("#1d4ed8"))
        c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + w / 2, y + h - 16, title)
        c.setFillColor(colors.white)
        c.rect(x, y, w, h - header_h, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        for i, row in enumerate(rows):
            row_y = y + h - header_h - row_h * (i + 1)
            c.line(x, row_y, x + w, row_y)
            c.setFillColor(colors.HexColor("#111827"))
            c.setFont("Helvetica", 8.8)
            c.drawString(x + 8, row_y + 6, row)
        c.setStrokeColor(colors.HexColor("#334155"))
        c.roundRect(x, y, w, h, 5, fill=0, stroke=1)
        return h

    def draw(self):
        c = self.canv
        left_x = 0.25 * inch
        right_x = 4.05 * inch
        y = 0.55 * inch
        table_w = 2.25 * inch
        self.draw_table(
            c,
            left_x,
            y,
            table_w,
            "AUTHOR",
            ["id  PK, identity", "name  NOT NULL", "books  mappedBy"],
        )
        self.draw_table(
            c,
            right_x,
            y,
            table_w,
            "BOOK",
            [
                "id  PK, identity",
                "title  UNIQUE, NOT NULL",
                "genre",
                "author_id  FK -> author.id",
            ],
        )
        c.setStrokeColor(colors.HexColor("#1d4ed8"))
        c.setLineWidth(1.4)
        c.line(left_x + table_w, y + 53, right_x, y + 53)
        c.setFillColor(colors.HexColor("#1d4ed8"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(left_x + table_w + 12, y + 64, "1")
        c.drawString(right_x - 24, y + 64, "many")
        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawCentredString(3.25 * inch, y + 34, "One author can have many books")


def table(data, col_widths):
    converted = []
    for row_index, row in enumerate(data):
        style_name = "TableHead" if row_index == 0 else "TableCell"
        converted.append([p(cell, style_name) for cell in row])
    t = Table(converted, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ]
        )
    )
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(doc.leftMargin, 0.38 * inch, "Library Management System - Project Report")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


story = []

story += [
    p("Library Management System", "TitleCenter"),
    p(
        "Project approach report covering ER design, operation implementation, code excerpts, screenshots, challenges, and testing evidence.",
        "Subtitle",
    ),
    p("1. Project Overview", "Section"),
    p(
        "This project is a Spring Boot MVC web application for maintaining a simple library book catalog. "
        "It uses Spring Data JPA with Hibernate for persistence, an H2 in-memory database for development, "
        "JSP views for the user interface, and Maven for building and testing.",
    ),
    bullets(
        [
            "<b>Backend:</b> Spring Boot 4.0.6, Spring MVC, Spring Data JPA, Hibernate.",
            "<b>Database:</b> H2 in-memory database at <font name='Courier'>jdbc:h2:mem:librarydb</font>.",
            "<b>Frontend:</b> JSP files under <font name='Courier'>src/main/webapp/WEB-INF/jsp</font> with embedded CSS.",
            "<b>Main feature set:</b> list books with authors, add a book, edit an existing book, and show a clear error for duplicate or empty book titles.",
        ]
    ),
    p("2. Entity Relationship Design", "Section"),
    p(
        "The database model is intentionally compact: authors are stored separately from books, and every book must belong to one author. "
        "This avoids repeating author names for every book and gives the project a clean one-to-many relationship."
    ),
    ERDiagram(),
    Spacer(1, 12),
    table(
        [
            ["Entity", "Important Fields", "Constraints / Relationship"],
            ["Author", "id, name, books", "id is the primary key. name is required. One Author has many Book records."],
            ["Book", "id, title, genre, author", "id is the primary key. title is required and unique. author_id is a required foreign key."],
        ],
        [1.2 * inch, 2.1 * inch, 3.25 * inch],
    ),
    Spacer(1, 8),
    code_block(
        "Entity mapping: src/main/java/com/example/library/entity/Author.java",
        """
        @Entity
        public class Author {
            @Id
            @GeneratedValue(strategy = GenerationType.IDENTITY)
            private Long id;

            @Column(nullable = false)
            private String name;

            @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
            private List<Book> books;
        }
        """,
    ),
    code_block(
        "Entity mapping: src/main/java/com/example/library/entity/Book.java",
        """
        @Entity
        public class Book {
            @Id
            @GeneratedValue(strategy = GenerationType.IDENTITY)
            private Long id;

            @Column(nullable = false, unique = true)
            private String title;

            private String genre;

            @ManyToOne
            @JoinColumn(name = "author_id", nullable = false)
            private Author author;
        }
        """,
    ),
    p("3. Implementation Details for Each Operation", "Section"),
    p("3.1 Read Operation: List Books with Authors", "Subsection"),
    p(
        "The list page is served by <font name='Courier'>GET /books</font>. The controller asks the service for all books, "
        "the service delegates to a custom repository query, and the JSP renders each book with its nested author name."
    ),
    code_block(
        "Controller + service + repository flow",
        """
        @GetMapping
        public String listBooks(Model model) {
            model.addAttribute("books", libraryService.getAllBooksWithAuthors());
            return "list-books";
        }

        public List<Book> getAllBooksWithAuthors() {
            return bookRepository.findAllBooksWithAuthorsInnerJoin();
        }

        @Query("SELECT b FROM Book b INNER JOIN FETCH b.author")
        List<Book> findAllBooksWithAuthorsInnerJoin();
        """,
    ),
    screenshot("01-book-list.png", "Screenshot 1: Book catalog rendered from seeded H2 data using the inner join query."),
    p("3.2 Create Operation: Show Add Book Form", "Subsection"),
    p(
        "The add form is served by <font name='Courier'>GET /books/new</font>. The controller sends an empty "
        "<font name='Courier'>Book</font> object for Spring form binding and all authors for the author dropdown."
    ),
    code_block(
        "Controller code for opening the create form",
        """
        @GetMapping("/new")
        public String showAddForm(Model model) {
            model.addAttribute("book", new Book());
            model.addAttribute("authors", libraryService.getAllAuthors());
            return "book-form";
        }
        """,
    ),
    code_block(
        "JSP form binding: src/main/webapp/WEB-INF/jsp/book-form.jsp",
        """
        <form:form action="/books/save" modelAttribute="book" method="POST">
            <form:hidden path="id" />
            <form:input path="title" required="required" placeholder="Enter book title" />
            <form:input path="genre" required="required" placeholder="Enter genre" />
            <form:select path="author.id">
                <form:option value="" label="-- Select an Author --" />
                <c:forEach var="auth" items="${authors}">
                    <form:option value="${auth.id}">${auth.name}</form:option>
                </c:forEach>
            </form:select>
        </form:form>
        """,
    ),
    screenshot("02-add-book-form.png", "Screenshot 2: Add New Book form with title, genre, and author dropdown."),
    p("3.3 Save Operation: Insert a New Book", "Subsection"),
    p(
        "The same <font name='Courier'>POST /books/save</font> endpoint handles saving. When the submitted book has no id, "
        "Spring Data JPA treats <font name='Courier'>bookRepository.save(book)</font> as an insert. A flash message is used after redirect so the user sees confirmation on the list page."
    ),
    code_block(
        "POST handler and service save method",
        """
        @PostMapping("/save")
        public String saveBook(@ModelAttribute("book") Book book,
                               RedirectAttributes redirectAttributes) {
            try {
                libraryService.saveBook(book);
                redirectAttributes.addFlashAttribute("success", "Book saved successfully!");
            } catch (RuntimeException e) {
                redirectAttributes.addFlashAttribute("error", e.getMessage());
                return "redirect:/books/new";
            }
            return "redirect:/books";
        }

        public void saveBook(Book book) {
            bookRepository.save(book);
        }
        """,
    ),
    screenshot("03-create-success.png", "Screenshot 3: Successful create operation redirects back to the catalog with a success message."),
    p("3.4 Update Operation: Edit an Existing Book", "Subsection"),
    p(
        "The edit form is served by <font name='Courier'>GET /books/edit/{id}</font>. The controller loads the existing book "
        "and reuses the same JSP. Because the form includes a hidden id field, the save endpoint performs an update instead of an insert."
    ),
    code_block(
        "Controller code for opening the edit form",
        """
        @GetMapping("/edit/{id}")
        public String showEditForm(@PathVariable Long id, Model model) {
            model.addAttribute("book", libraryService.getBookById(id));
            model.addAttribute("authors", libraryService.getAllAuthors());
            return "book-form";
        }

        public Book getBookById(Long id) {
            return bookRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Book with ID " + id + " not found"));
        }
        """,
    ),
    screenshot("04-edit-book-form.png", "Screenshot 4: The same form is reused for updating an existing book."),
    p("3.5 Data Integrity Handling", "Subsection"),
    p(
        "The <font name='Courier'>Book.title</font> column is both required and unique. If the database rejects a duplicate title, "
        "the service catches the Spring data exception and returns a friendly message to the form instead of exposing a raw SQL error."
    ),
    code_block(
        "Friendly integrity handling in LibraryService",
        """
        public void saveBook(Book book) {
            try {
                bookRepository.save(book);
            } catch (DataIntegrityViolationException e) {
                throw new RuntimeException(
                    "Data integrity violation: Book title must be unique and cannot be empty."
                );
            }
        }
        """,
    ),
    screenshot("05-data-integrity-error.png", "Screenshot 5: Duplicate title submission is rejected and shown as a clear validation message."),
    PageBreak(),
    p("4. Database Initialization", "Section"),
    p(
        "The application uses <font name='Courier'>spring.jpa.hibernate.ddl-auto=update</font> so Hibernate creates or updates the schema from the entity classes. "
        "The <font name='Courier'>data.sql</font> file seeds 10 authors and 10 books. "
        "<font name='Courier'>spring.jpa.defer-datasource-initialization=true</font> ensures the schema exists before seed data is inserted."
    ),
    code_block(
        "Configuration: src/main/resources/application.properties",
        """
        spring.datasource.url=jdbc:h2:mem:librarydb
        spring.datasource.driverClassName=org.h2.Driver
        spring.datasource.username=sa
        spring.jpa.hibernate.ddl-auto=update
        spring.h2.console.enabled=true
        spring.mvc.view.prefix=/WEB-INF/jsp/
        spring.mvc.view.suffix=.jsp
        spring.jpa.defer-datasource-initialization=true
        """,
    ),
    code_block(
        "Seed data example: src/main/resources/data.sql",
        """
        INSERT INTO author (name) VALUES ('George Orwell');
        INSERT INTO author (name) VALUES ('J.K. Rowling');

        INSERT INTO book (title, genre, author_id)
        VALUES ('1984', 'Dystopian', 1);
        INSERT INTO book (title, genre, author_id)
        VALUES ('Harry Potter and the Sorcerer''s Stone', 'Fantasy', 2);
        """,
    ),
    p("5. Challenges Faced and How They Were Overcome", "Section"),
    table(
        [
            ["Challenge", "How it was handled"],
            [
                "Representing the author-book relationship cleanly",
                "Separated Author and Book into two JPA entities. Book owns the foreign key with @ManyToOne and @JoinColumn, while Author exposes the inverse @OneToMany relationship.",
            ],
            [
                "Displaying author details without extra queries",
                "Used an explicit JPQL INNER JOIN FETCH query so the list page receives books and authors in one query.",
            ],
            [
                "Binding a selected author from a JSP dropdown",
                "Used Spring form binding with path=\"author.id\", allowing the selected author id to be bound into the Book object.",
            ],
            [
                "Showing validation errors clearly",
                "Added a unique and not-null constraint on title, caught DataIntegrityViolationException in the service, and displayed a friendly flash error on the form.",
            ],
            [
                "Running JSPs in embedded Tomcat",
                "Added Jasper and JSTL dependencies in pom.xml, then configured the MVC view prefix and suffix for /WEB-INF/jsp/.",
            ],
            [
                "Loading seed data reliably",
                "Enabled deferred datasource initialization so data.sql runs after Hibernate creates the tables.",
            ],
        ],
        [2.2 * inch, 4.35 * inch],
    ),
    Spacer(1, 10),
    p("6. Testing and Verification", "Section"),
    p(
        "The project includes Spring Boot tests for context loading and service behavior. The service tests verify that seeded books are returned, "
        "book id lookup works, authors are loaded, and duplicate titles produce the expected friendly error message."
    ),
    code_block(
        "Test evidence: src/test/java/com/example/library/service/LibraryServiceTest.java",
        """
        @Test
        void getAllBooksWithAuthorsReturnsSeededBooks() {
            List<Book> books = libraryService.getAllBooksWithAuthors();
            assertFalse(books.isEmpty());
            assertTrue(books.stream().anyMatch(book -> "1984".equals(book.getTitle())));
            assertTrue(books.stream().allMatch(book -> book.getAuthor() != null));
        }

        @Test
        void saveBookThrowsFriendlyMessageOnIntegrityViolation() {
            Author author = libraryService.getAllAuthors().get(0);
            Book duplicate = new Book("1984", "Dystopian", author);
            RuntimeException exception = assertThrows(
                RuntimeException.class,
                () -> libraryService.saveBook(duplicate)
            );
            assertEquals(
                "Data integrity violation: Book title must be unique and cannot be empty.",
                exception.getMessage()
            );
        }
        """,
    ),
    p(
        "Verification run: <font name='Courier'>./mvnw test</font> completed successfully with "
        "<b>4 tests run, 0 failures, 0 errors, 0 skipped</b>.",
    ),
    p("7. Conclusion", "Section"),
    p(
        "The project demonstrates a complete database-backed MVC flow for a library catalog: normalized entity design, "
        "Spring Data repository access, service-layer validation handling, JSP form binding, and visible user feedback. "
        "The design can be extended naturally with delete operations, search/filtering, server-side validation annotations, and a persistent production database."
    ),
]


def build():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Library Project Report",
        author="Library Management System",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(PDF_PATH)
