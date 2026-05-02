<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <title>Authors</title>
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
        <h2>Authors</h2>
        <a class="btn btn-success" href="/authors/new">+ New Author</a>
    </div>

    <c:if test="${not empty message}">
        <div class="alert alert-success">${message}</div>
    </c:if>

    <table>
        <thead>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Nationality</th><th>Actions</th></tr>
        </thead>
        <tbody>
        <c:forEach var="a" items="${authors}">
            <tr>
                <td>${a.id}</td>
                <td><c:out value="${a.name}"/></td>
                <td><c:out value="${a.email}"/></td>
                <td><c:out value="${a.nationality}"/></td>
                <td><a class="btn btn-small" href="/authors/${a.id}/edit">Edit</a></td>
            </tr>
        </c:forEach>
        <c:if test="${empty authors}">
            <tr><td colspan="5" style="text-align:center;color:#6b7280;">No authors yet.</td></tr>
        </c:if>
        </tbody>
    </table>
</main>
</body>
</html>
