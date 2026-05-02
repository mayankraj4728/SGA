<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <title>Books + Authors (Inner Join)</title>
    <link rel="stylesheet" href="/css/styles.css"/>
</head>
<body>
<header><h1>SGA Library Management</h1></header>
<nav>
    <a href="/">Home</a>
    <a href="/authors">Authors</a>
    <a href="/books">Books</a>
    <a href="/books/with-authors">Books + Authors (Inner Join)</a>
</nav>
<main>
    <h2>Books joined with Authors</h2>
    <p style="color:#6b7280;">Result of the custom JPQL <code>INNER JOIN</code> query in <code>BookRepository.findAllBooksWithAuthors()</code>.</p>

    <table>
        <thead>
        <tr>
            <th>Book ID</th><th>Title</th><th>ISBN</th><th>Genre</th><th>Price</th>
            <th>Author</th><th>Email</th><th>Nationality</th>
        </tr>
        </thead>
        <tbody>
        <c:forEach var="r" items="${rows}">
            <tr>
                <td>${r.bookId}</td>
                <td><c:out value="${r.title}"/></td>
                <td><c:out value="${r.isbn}"/></td>
                <td><c:out value="${r.genre}"/></td>
                <td>$<c:out value="${r.price}"/></td>
                <td><c:out value="${r.authorName}"/></td>
                <td><c:out value="${r.authorEmail}"/></td>
                <td><c:out value="${r.authorNationality}"/></td>
            </tr>
        </c:forEach>
        <c:if test="${empty rows}">
            <tr><td colspan="8" style="text-align:center;color:#6b7280;">No data.</td></tr>
        </c:if>
        </tbody>
    </table>
</main>
</body>
</html>
