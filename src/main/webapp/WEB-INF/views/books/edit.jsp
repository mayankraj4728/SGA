<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <title>Edit Book</title>
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
    <h2>Edit Book</h2>

    <c:if test="${not empty error}">
        <div class="alert alert-error">${error}</div>
    </c:if>

    <div class="card">
        <form:form modelAttribute="book" method="post" action="/books/${book.id}">
            <div class="field">
                <label>Title</label>
                <form:input path="title"/>
                <form:errors path="title" cssClass="field-error"/>
            </div>
            <div class="field">
                <label>ISBN</label>
                <form:input path="isbn"/>
                <form:errors path="isbn" cssClass="field-error"/>
            </div>
            <div class="field">
                <label>Genre</label>
                <form:input path="genre"/>
            </div>
            <div class="field">
                <label>Price</label>
                <form:input path="price" type="number" step="0.01"/>
                <form:errors path="price" cssClass="field-error"/>
            </div>
            <div class="field">
                <label>Author</label>
                <select name="authorId" required>
                    <c:forEach var="a" items="${authors}">
                        <option value="${a.id}" <c:if test="${a.id == book.author.id}">selected</c:if>>
                            <c:out value="${a.name}"/>
                        </option>
                    </c:forEach>
                </select>
            </div>
            <div class="actions">
                <button type="submit" class="btn">Save Changes</button>
                <a href="/books" class="btn btn-secondary">Cancel</a>
            </div>
        </form:form>
    </div>
</main>
</body>
</html>
