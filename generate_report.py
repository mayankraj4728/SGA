"""Generate the SGA Library project submission PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable
)
from reportlab.pdfgen import canvas
from reportlab.lib import colors


PRIMARY = HexColor("#1e3a8a")
ACCENT = HexColor("#2563eb")
MUTED = HexColor("#6b7280")
CODE_BG = HexColor("#f3f4f6")
PLACEHOLDER_BG = HexColor("#fafbff")
PLACEHOLDER_BORDER = HexColor("#94a3b8")


styles = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=styles["Heading1"],
                    fontName="Helvetica-Bold", fontSize=22, leading=28,
                    textColor=PRIMARY, spaceBefore=6, spaceAfter=12)
H2 = ParagraphStyle("H2", parent=styles["Heading2"],
                    fontName="Helvetica-Bold", fontSize=15, leading=20,
                    textColor=PRIMARY, spaceBefore=14, spaceAfter=8)
H3 = ParagraphStyle("H3", parent=styles["Heading3"],
                    fontName="Helvetica-Bold", fontSize=12, leading=16,
                    textColor=ACCENT, spaceBefore=10, spaceAfter=6)
BODY = ParagraphStyle("Body", parent=styles["BodyText"],
                      fontName="Helvetica", fontSize=10.5, leading=15,
                      alignment=TA_JUSTIFY, spaceAfter=8)
BULLET = ParagraphStyle("Bullet", parent=BODY,
                        leftIndent=18, bulletIndent=6, spaceAfter=4)
CODE = ParagraphStyle("Code", parent=styles["Code"],
                      fontName="Courier", fontSize=8.6, leading=11,
                      backColor=CODE_BG, borderColor=HexColor("#d1d5db"),
                      borderWidth=0.5, borderPadding=8,
                      leftIndent=0, rightIndent=0, spaceAfter=10)
CAPTION = ParagraphStyle("Caption", parent=BODY,
                         fontSize=9, textColor=MUTED, alignment=TA_CENTER,
                         spaceBefore=4, spaceAfter=12)
SUBTITLE = ParagraphStyle("Subtitle", parent=BODY,
                          fontSize=12, alignment=TA_CENTER, textColor=MUTED,
                          spaceAfter=20)


def code(s: str) -> Paragraph:
    """Render a code snippet, escaping HTML chars and preserving whitespace."""
    s = (s.replace("&", "&amp;")
          .replace("<", "&lt;")
          .replace(">", "&gt;")
          .replace(" ", "&nbsp;")
          .replace("\n", "<br/>"))
    return Paragraph(s, CODE)


class ScreenshotPlaceholder(Flowable):
    """A bordered, dashed rectangle with a centred caption — leaves space for the user's screenshot."""

    def __init__(self, label: str, height_cm: float = 7.5, width_cm: float = 16.0):
        super().__init__()
        self.label = label
        self.height = height_cm * cm
        self.width = width_cm * cm

    def wrap(self, available_width, available_height):
        self.width = min(self.width, available_width)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(PLACEHOLDER_BG)
        c.setStrokeColor(PLACEHOLDER_BORDER)
        c.setDash(4, 3)
        c.setLineWidth(0.8)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=1)
        c.setDash()

        c.setFillColor(MUTED)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(self.width / 2, self.height / 2 + 6, "[ Insert screenshot here ]")
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(self.width / 2, self.height / 2 - 8, self.label)
        c.restoreState()


def header_footer(canv: canvas.Canvas, doc):
    canv.saveState()
    # Header
    canv.setFillColor(PRIMARY)
    canv.rect(0, A4[1] - 1.2 * cm, A4[0], 1.2 * cm, stroke=0, fill=1)
    canv.setFillColor(colors.white)
    canv.setFont("Helvetica-Bold", 10)
    canv.drawString(2 * cm, A4[1] - 0.8 * cm, "SGA Library Management — Project Report")
    canv.setFont("Helvetica", 9)
    canv.drawRightString(A4[0] - 2 * cm, A4[1] - 0.8 * cm, "Spring Boot CRUD")

    # Footer
    canv.setFillColor(MUTED)
    canv.setFont("Helvetica", 9)
    canv.drawCentredString(A4[0] / 2, 1.1 * cm, f"Page {doc.page}")
    canv.restoreState()


def cover(story):
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph("SGA Database System", H1))
    story.append(Paragraph("Spring Boot CRUD Application — Authors &amp; Books", SUBTITLE))
    story.append(Spacer(1, 1.5 * cm))

    info = [
        ["Project", "SGA Library Management"],
        ["Stack", "Spring Boot 3.2.5, Spring Data JPA, JSP, JSTL, H2"],
        ["Language", "Java 17"],
        ["Build Tool", "Maven"],
        ["Tests", "JUnit 5 + Mockito (16 tests, all passing)"],
        ["Author", "_______________________________"],
        ["Date", "_______________________________"],
        ["GitHub URL", "_______________________________"],
    ]
    t = Table(info, colWidths=[4.5 * cm, 11 * cm])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("TEXTCOLOR", (0, 0), (0, -1), PRIMARY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, HexColor("#e5e7eb")),
    ]))
    story.append(t)
    story.append(PageBreak())


def overview(story):
    story.append(Paragraph("1. Project Overview", H2))
    story.append(Paragraph(
        "This project is a Spring Boot web application that manages information for two related entities: "
        "<b>Authors</b> and <b>Books</b>. It implements three CRUD operations — <b>Create</b>, <b>Read</b>, "
        "and <b>Update</b> — through a layered architecture (entity, repository, service, controller, view) and "
        "exposes the functionality via JSP pages styled with custom CSS. The data layer uses an H2 in-memory "
        "database, and the application is seeded with 10 authors and 10 books on startup. The repository layer "
        "additionally exposes a custom JPQL <b>INNER JOIN</b> query that returns books together with their "
        "authors as a flat projection.",
        BODY))
    story.append(Paragraph(
        "Unit tests cover the repository layer (using <i>@DataJpaTest</i> against an embedded H2) and the "
        "service layer (using Mockito), including data-integrity-violation scenarios.",
        BODY))


def er_design(story):
    story.append(Paragraph("2. Entity Relationship Design", H2))
    story.append(Paragraph(
        "The two chosen entities are related as <b>One Author has Many Books</b>, and <b>each Book belongs to "
        "exactly one Author</b>. This is modelled as a bidirectional JPA association: <i>@OneToMany</i> on the "
        "Author side and <i>@ManyToOne</i> on the Book side, with the Book table owning the foreign key column "
        "<i>author_id</i>.",
        BODY))

    story.append(Paragraph("Diagram", H3))
    story.append(code(
        "+-----------------------+         +--------------------------+\n"
        "|        Author         | 1     N |          Book            |\n"
        "+-----------------------+---------+--------------------------+\n"
        "| id        BIGINT (PK) |         | id         BIGINT (PK)   |\n"
        "| name      VARCHAR     |<--------| author_id  BIGINT (FK)   |\n"
        "| email     VARCHAR (U) |         | title      VARCHAR       |\n"
        "| nationality VARCHAR   |         | isbn       VARCHAR (U)   |\n"
        "+-----------------------+         | genre      VARCHAR       |\n"
        "                                  | price      DOUBLE        |\n"
        "                                  +--------------------------+\n"
        "(U) = UNIQUE constraint        (FK) = foreign key on author_id"
    ))

    story.append(Paragraph("Constraints &amp; Validation", H3))
    story.append(Paragraph("- Author.email is <b>unique</b> and not null.", BULLET))
    story.append(Paragraph("- Book.isbn is <b>unique</b> and not null.", BULLET))
    story.append(Paragraph("- Book.author_id is a non-null foreign key — every book must reference an author.", BULLET))
    story.append(Paragraph("- Bean Validation annotations (<i>@NotBlank</i>, <i>@Positive</i>, <i>@Size</i>) enforce field-level rules.", BULLET))
    story.append(Paragraph("- Cascade <i>ALL</i> with orphan removal on the Author→Books side keeps the children consistent with their parent.", BULLET))

    story.append(Paragraph("Author entity (excerpt)", H3))
    story.append(code(
        "@Entity\n"
        "@Table(name = \"authors\",\n"
        "       uniqueConstraints = @UniqueConstraint(columnNames = \"email\"))\n"
        "public class Author {\n"
        "    @Id\n"
        "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
        "    private Long id;\n\n"
        "    @NotBlank @Size(max = 100)\n"
        "    @Column(nullable = false, length = 100)\n"
        "    private String name;\n\n"
        "    @NotBlank\n"
        "    @Column(nullable = false, unique = true, length = 150)\n"
        "    private String email;\n\n"
        "    @Column(length = 60)\n"
        "    private String nationality;\n\n"
        "    @OneToMany(mappedBy = \"author\", cascade = CascadeType.ALL,\n"
        "               orphanRemoval = true, fetch = FetchType.LAZY)\n"
        "    private List<Book> books = new ArrayList<>();\n"
        "}"
    ))

    story.append(Paragraph("Book entity (excerpt)", H3))
    story.append(code(
        "@Entity\n"
        "@Table(name = \"books\",\n"
        "       uniqueConstraints = @UniqueConstraint(columnNames = \"isbn\"))\n"
        "public class Book {\n"
        "    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
        "    private Long id;\n\n"
        "    @NotBlank @Column(nullable = false, length = 200)\n"
        "    private String title;\n\n"
        "    @NotBlank @Column(nullable = false, unique = true, length = 20)\n"
        "    private String isbn;\n\n"
        "    @Column(length = 60) private String genre;\n\n"
        "    @NotNull @Positive @Column(nullable = false)\n"
        "    private Double price;\n\n"
        "    @ManyToOne(fetch = FetchType.LAZY, optional = false)\n"
        "    @JoinColumn(name = \"author_id\", nullable = false)\n"
        "    private Author author;\n"
        "}"
    ))

    story.append(PageBreak())


def populate_section(story):
    story.append(Paragraph("3. Database Population (Sample Data)", H2))
    story.append(Paragraph(
        "On application startup, a Spring <i>CommandLineRunner</i> bean (<b>DataInitializer</b>) inserts "
        "10 authors and 10 books if the tables are empty. This seeds the DB so the JSP listings have "
        "content immediately.",
        BODY))
    story.append(code(
        "@Bean\n"
        "CommandLineRunner seedDatabase(AuthorRepository authorRepo,\n"
        "                               BookRepository bookRepo) {\n"
        "    return args -> {\n"
        "        if (authorRepo.count() > 0) return;\n"
        "        List<Author> authors = List.of(\n"
        "            new Author(\"George Orwell\", \"...\", \"British\"),\n"
        "            new Author(\"Jane Austen\",   \"...\", \"British\"),\n"
        "            /* ... 10 authors total ... */);\n"
        "        authorRepo.saveAll(authors);\n"
        "        List<Book> books = List.of(\n"
        "            new Book(\"1984\", \"978-0451524935\",\n"
        "                     \"Dystopian\", 14.99, authors.get(0)),\n"
        "            /* ... 10 books total, each linked to an author ... */);\n"
        "        bookRepo.saveAll(books);\n"
        "    };\n"
        "}"
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(ScreenshotPlaceholder("Figure 1 — H2 console showing populated AUTHORS and BOOKS tables"))
    story.append(Paragraph(
        "Tip: open <i>http://localhost:8080/h2-console</i> with JDBC URL "
        "<i>jdbc:h2:mem:librarydb</i> to take this screenshot.",
        CAPTION))
    story.append(PageBreak())


def create_section(story):
    story.append(Paragraph("4. Create Operation", H2))
    story.append(Paragraph(
        "The Create flow is implemented as an HTML form rendered by a JSP, submitted to a controller "
        "method that delegates to the service layer, which in turn persists the entity through the "
        "repository. Bean Validation annotations are evaluated on submission, and "
        "<i>DataIntegrityViolationException</i> is caught explicitly so that duplicate-email or "
        "duplicate-ISBN attempts surface a friendly inline message rather than a 500 page.",
        BODY))

    story.append(Paragraph("Controller", H3))
    story.append(code(
        "@PostMapping\n"
        "public String create(@Valid @ModelAttribute(\"book\") Book book,\n"
        "                     BindingResult result,\n"
        "                     @RequestParam(\"authorId\") Long authorId,\n"
        "                     Model model,\n"
        "                     RedirectAttributes redirectAttrs) {\n"
        "    if (result.hasErrors()) {\n"
        "        model.addAttribute(\"authors\", authorService.findAll());\n"
        "        return \"books/form\";\n"
        "    }\n"
        "    try {\n"
        "        bookService.create(book, authorId);\n"
        "        redirectAttrs.addFlashAttribute(\n"
        "            \"message\", \"Book created successfully.\");\n"
        "        return \"redirect:/books\";\n"
        "    } catch (DataIntegrityViolationException ex) {\n"
        "        model.addAttribute(\"authors\", authorService.findAll());\n"
        "        model.addAttribute(\"error\", ex.getMessage());\n"
        "        return \"books/form\";\n"
        "    }\n"
        "}"
    ))

    story.append(Paragraph("Service (integrity-violation translation)", H3))
    story.append(code(
        "public Book create(Book book, Long authorId) {\n"
        "    Author author = authorService.findById(authorId);\n"
        "    book.setAuthor(author);\n"
        "    try {\n"
        "        return bookRepository.save(book);\n"
        "    } catch (DataIntegrityViolationException ex) {\n"
        "        throw new DataIntegrityViolationException(\n"
        "          \"Could not save book: a book with ISBN '\"\n"
        "             + book.getIsbn() + \"' already exists.\", ex);\n"
        "    }\n"
        "}"
    ))

    story.append(Paragraph("JSP form (excerpt)", H3))
    story.append(code(
        "<form:form modelAttribute=\"book\" method=\"post\" action=\"/books\">\n"
        "  <div class=\"field\">\n"
        "    <label>Title</label>\n"
        "    <form:input path=\"title\"/>\n"
        "    <form:errors path=\"title\" cssClass=\"field-error\"/>\n"
        "  </div>\n"
        "  <!-- isbn, genre, price, author fields ... -->\n"
        "  <button type=\"submit\" class=\"btn\">Create Book</button>\n"
        "</form:form>"
    ))

    story.append(ScreenshotPlaceholder("Figure 2 — Add New Book form (/books/new)"))
    story.append(ScreenshotPlaceholder("Figure 3 — Add New Author form (/authors/new)"))
    story.append(ScreenshotPlaceholder(
        "Figure 4 — Inline error after submitting a duplicate ISBN (data-integrity violation)"))
    story.append(PageBreak())


def read_section(story):
    story.append(Paragraph("5. Read Operation", H2))
    story.append(Paragraph(
        "Two list pages are provided. <b>/books</b> and <b>/authors</b> render plain entity lists from "
        "<i>findAll()</i>. A third page, <b>/books/with-authors</b>, renders the result of a custom "
        "JPQL inner-join query, projecting both Book and Author columns into a flat DTO "
        "(<i>BookAuthorView</i>). This satisfies the requirement to expose a custom repository query "
        "that joins the two entities.",
        BODY))

    story.append(Paragraph("Controller", H3))
    story.append(code(
        "@GetMapping\n"
        "public String list(Model model) {\n"
        "    model.addAttribute(\"books\", bookService.findAll());\n"
        "    return \"books/list\";\n"
        "}\n\n"
        "@GetMapping(\"/with-authors\")\n"
        "public String listWithAuthors(Model model) {\n"
        "    model.addAttribute(\"rows\", bookService.findAllBooksWithAuthors());\n"
        "    return \"books/with-authors\";\n"
        "}"
    ))

    story.append(Paragraph("JSP listing (binding via JSTL)", H3))
    story.append(code(
        "<table>\n"
        "  <thead><tr><th>ID</th><th>Title</th><th>ISBN</th>\n"
        "             <th>Author</th><th>Actions</th></tr></thead>\n"
        "  <tbody>\n"
        "  <c:forEach var=\"b\" items=\"${books}\">\n"
        "    <tr>\n"
        "      <td>${b.id}</td>\n"
        "      <td><c:out value=\"${b.title}\"/></td>\n"
        "      <td><c:out value=\"${b.isbn}\"/></td>\n"
        "      <td><c:out value=\"${b.author.name}\"/></td>\n"
        "      <td><a class=\"btn btn-small\"\n"
        "             href=\"/books/${b.id}/edit\">Edit</a></td>\n"
        "    </tr>\n"
        "  </c:forEach>\n"
        "  </tbody>\n"
        "</table>"
    ))

    story.append(ScreenshotPlaceholder("Figure 5 — Author list page (/authors)"))
    story.append(ScreenshotPlaceholder("Figure 6 — Book list page (/books)"))
    story.append(PageBreak())


def join_section(story):
    story.append(Paragraph("6. Custom Inner-Join Query", H2))
    story.append(Paragraph(
        "The repository defines a JPQL query using <b>INNER JOIN</b> on the <i>book.author</i> "
        "association, projecting columns from both entities into a constructor-expression DTO. This "
        "means only one round-trip to the database, no lazy-loading per row, and the result is "
        "shaped exactly the way the JSP needs it.",
        BODY))

    story.append(Paragraph("Repository method", H3))
    story.append(code(
        "@Query(\"\"\"\n"
        "    SELECT new com.sga.library.dto.BookAuthorView(\n"
        "        b.id, b.title, b.isbn, b.genre, b.price,\n"
        "        a.id, a.name, a.email, a.nationality)\n"
        "    FROM Book b\n"
        "    INNER JOIN b.author a\n"
        "    ORDER BY a.name ASC, b.title ASC\n"
        "    \"\"\")\n"
        "List<BookAuthorView> findAllBooksWithAuthors();"
    ))

    story.append(Paragraph("Generated SQL (from Hibernate)", H3))
    story.append(code(
        "SELECT b1_0.id, b1_0.title, b1_0.isbn, b1_0.genre, b1_0.price,\n"
        "       a1_0.id, a1_0.name, a1_0.email, a1_0.nationality\n"
        "FROM   books b1_0\n"
        "JOIN   authors a1_0 ON a1_0.id = b1_0.author_id\n"
        "ORDER  BY a1_0.name, b1_0.title;"
    ))

    story.append(Paragraph("BookAuthorView DTO", H3))
    story.append(code(
        "public class BookAuthorView {\n"
        "    private final Long bookId;\n"
        "    private final String title, isbn, genre;\n"
        "    private final Double price;\n"
        "    private final Long authorId;\n"
        "    private final String authorName, authorEmail, authorNationality;\n\n"
        "    // constructor matching the SELECT new ... in JPQL\n"
        "    // + getters\n"
        "}"
    ))

    story.append(ScreenshotPlaceholder(
        "Figure 7 — Books + Authors inner-join page (/books/with-authors)"))
    story.append(PageBreak())


def update_section(story):
    story.append(Paragraph("7. Update Operation", H2))
    story.append(Paragraph(
        "Each list page exposes an Edit button that loads a pre-populated form. The same controller "
        "pattern (POST + redirect-after-submit) is reused. The service fetches the persisted entity, "
        "applies the form fields, and saves — keeping the JPA identity stable. Integrity violations "
        "(e.g. assigning an ISBN that already belongs to another book) are caught and re-rendered "
        "as inline form errors.",
        BODY))

    story.append(Paragraph("Controller", H3))
    story.append(code(
        "@PostMapping(\"/{id}\")\n"
        "public String update(@PathVariable Long id,\n"
        "                     @Valid @ModelAttribute(\"book\") Book book,\n"
        "                     BindingResult result,\n"
        "                     @RequestParam(\"authorId\") Long authorId,\n"
        "                     Model model,\n"
        "                     RedirectAttributes redirectAttrs) {\n"
        "    if (result.hasErrors()) {\n"
        "        model.addAttribute(\"authors\", authorService.findAll());\n"
        "        return \"books/edit\";\n"
        "    }\n"
        "    try {\n"
        "        bookService.update(id, book, authorId);\n"
        "        redirectAttrs.addFlashAttribute(\"message\",\n"
        "            \"Book updated successfully.\");\n"
        "        return \"redirect:/books\";\n"
        "    } catch (DataIntegrityViolationException ex) {\n"
        "        model.addAttribute(\"authors\", authorService.findAll());\n"
        "        model.addAttribute(\"error\", ex.getMessage());\n"
        "        return \"books/edit\";\n"
        "    }\n"
        "}"
    ))

    story.append(Paragraph("Service", H3))
    story.append(code(
        "public Book update(Long id, Book updated, Long authorId) {\n"
        "    Book existing = findById(id);\n"
        "    existing.setTitle(updated.getTitle());\n"
        "    existing.setIsbn(updated.getIsbn());\n"
        "    existing.setGenre(updated.getGenre());\n"
        "    existing.setPrice(updated.getPrice());\n"
        "    if (authorId != null) {\n"
        "        existing.setAuthor(authorService.findById(authorId));\n"
        "    }\n"
        "    return bookRepository.save(existing);\n"
        "}"
    ))

    story.append(ScreenshotPlaceholder("Figure 8 — Edit Book form pre-populated with existing data"))
    story.append(ScreenshotPlaceholder("Figure 9 — Book list reflecting the updated record"))
    story.append(PageBreak())


def testing_section(story):
    story.append(Paragraph("8. Testing &amp; Validation", H2))
    story.append(Paragraph(
        "The project ships with 16 unit tests across four classes. Repository tests use "
        "<i>@DataJpaTest</i> with Spring's auto-configured embedded H2 to verify the custom "
        "inner-join query and unique-constraint enforcement. Service tests use Mockito to isolate "
        "the business logic from the DB, including exception-translation paths.",
        BODY))

    story.append(Paragraph("Inner-join repository test", H3))
    story.append(code(
        "@DataJpaTest\n"
        "class BookRepositoryTest {\n"
        "    @Test\n"
        "    void findAllBooksWithAuthors_returnsInnerJoinedRows() {\n"
        "        Author a = authorRepository.save(\n"
        "            new Author(\"Alpha Author\", \"a@x.com\", \"USA\"));\n"
        "        bookRepository.save(\n"
        "            new Book(\"Alpha Book\", \"A-001\", \"Fiction\", 10.0, a));\n\n"
        "        List<BookAuthorView> rows =\n"
        "            bookRepository.findAllBooksWithAuthors();\n\n"
        "        assertThat(rows).hasSize(1);\n"
        "        assertThat(rows.get(0).getAuthorName())\n"
        "            .isEqualTo(\"Alpha Author\");\n"
        "    }\n"
        "}"
    ))

    story.append(Paragraph("Service-level integrity-violation test", H3))
    story.append(code(
        "@Test\n"
        "void create_translatesIntegrityViolation() {\n"
        "    when(authorService.findById(10L)).thenReturn(author);\n"
        "    when(bookRepository.save(any(Book.class)))\n"
        "        .thenThrow(new DataIntegrityViolationException(\"dup\"));\n\n"
        "    assertThatThrownBy(() -> bookService.create(input, 10L))\n"
        "        .isInstanceOf(DataIntegrityViolationException.class)\n"
        "        .hasMessageContaining(\"ISBN-DUP\");\n"
        "}"
    ))

    story.append(ScreenshotPlaceholder("Figure 10 — Maven test output: 16 tests passed", height_cm=6.5))
    story.append(PageBreak())


def challenges(story):
    story.append(Paragraph("9. Challenges Faced", H2))
    challenges_list = [
        ("JSP packaging with embedded Tomcat",
         "Spring Boot's default jar packaging does not serve JSPs from the classpath. Resolution: keep JSPs under "
         "<i>src/main/webapp/WEB-INF/views</i>, declare <i>tomcat-embed-jasper</i> with scope <i>provided</i>, and "
         "wire the view resolver via <i>spring.mvc.view.prefix</i> / <i>suffix</i> in <i>application.properties</i>."),
        ("Mapping the inner-join into a flat row",
         "Returning <i>List&lt;Object[]&gt;</i> from the join query forced index-based access in the JSP, which is "
         "fragile. Resolution: use a JPQL constructor expression "
         "(<i>SELECT new com.sga.library.dto.BookAuthorView(...)</i>) so the result is a typed DTO with proper "
         "getters, which the JSP renders cleanly via EL."),
        ("Distinguishing data-integrity violations from generic errors",
         "Saving a duplicate email or ISBN raised a low-level Hibernate exception that was not user-friendly. "
         "Resolution: wrap each <i>save()</i> in the service layer with a try/catch on "
         "<i>DataIntegrityViolationException</i> and re-throw a contextual message, then have controllers render it "
         "as an inline form error rather than crashing into a 500 page."),
        ("Avoiding lazy-loading issues in JSPs",
         "Rendering a list of books inside JSP triggered LazyInitializationException when the rendering happened "
         "outside an active session. Resolution: rely on <i>spring.jpa.open-in-view</i> for the simple list pages, "
         "and use the inner-join projection for the join page so the JSP never needs to traverse a lazy "
         "association."),
        ("Two-way relationship with Jackson serialisation",
         "The bidirectional Author ↔ Books relationship would have caused infinite recursion if exposed to JSON. "
         "Resolution: annotate the <i>books</i> collection on Author with <i>@JsonIgnore</i> so JSON callers see a "
         "clean Author payload while JPA still walks the relationship internally."),
    ]
    for title, body in challenges_list:
        story.append(Paragraph(f"<b>•&nbsp; {title}.</b> {body}", BODY))


def submission(story):
    story.append(Paragraph("10. Submission Details", H2))
    story.append(Paragraph(
        "<b>GitHub URL:</b> _________________________________________________________",
        BODY))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "<b>How to run locally</b>",
        H3))
    story.append(code(
        "git clone <github-url>\n"
        "cd library\n"
        "mvn spring-boot:run\n"
        "# then open http://localhost:8080/"
    ))
    story.append(Paragraph(
        "<b>How to run tests</b>", H3))
    story.append(code("mvn test    # 16 tests, all passing"))
    story.append(Paragraph(
        "<b>Useful URLs</b>", H3))
    story.append(Paragraph("- <b>/</b> — home", BULLET))
    story.append(Paragraph("- <b>/authors</b> — list / create / edit authors", BULLET))
    story.append(Paragraph("- <b>/books</b> — list / create / edit books", BULLET))
    story.append(Paragraph("- <b>/books/with-authors</b> — custom inner-join report", BULLET))
    story.append(Paragraph("- <b>/h2-console</b> — H2 web console (JDBC: jdbc:h2:mem:librarydb)", BULLET))


def build_pdf(out_path: str):
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="SGA Library — Project Report",
        author="SGA",
    )
    story = []
    cover(story)
    overview(story)
    er_design(story)
    populate_section(story)
    create_section(story)
    read_section(story)
    join_section(story)
    update_section(story)
    testing_section(story)
    challenges(story)
    submission(story)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("Generated:", out_path)


if __name__ == "__main__":
    build_pdf("/Users/mayankraj/Desktop/SGA/SGA_Library_Report.pdf")
