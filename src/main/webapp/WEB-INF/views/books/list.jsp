<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <title>Books</title>
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
    <div class="toolbar">
        <h2>Books</h2>
        <a class="btn btn-success" href="/books/new">+ New Book</a>
    </div>

    <c:if test="${not empty message}">
        <div class="alert alert-success">${message}</div>
    </c:if>

    <table>
        <thead>
        <tr><th>ID</th><th>Title</th><th>ISBN</th><th>Genre</th><th>Price</th><th>Author</th><th>Actions</th></tr>
        </thead>
        <tbody>
        <c:forEach var="b" items="${books}">
            <tr>
                <td>${b.id}</td>
                <td><c:out value="${b.title}"/></td>
                <td><c:out value="${b.isbn}"/></td>
                <td><c:out value="${b.genre}"/></td>
                <td>$<c:out value="${b.price}"/></td>
                <td><c:out value="${b.author.name}"/></td>
                <td><a class="btn btn-small" href="/books/${b.id}/edit">Edit</a></td>
            </tr>
        </c:forEach>
        <c:if test="${empty books}">
            <tr><td colspan="7" style="text-align:center;color:#6b7280;">No books yet.</td></tr>
        </c:if>
        </tbody>
    </table>
</main>
</body>
</html>
