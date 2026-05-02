<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!DOCTYPE html>
<html>
<head>
    <title>New Author</title>
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
    <h2>Add New Author</h2>

    <c:if test="${not empty error}">
        <div class="alert alert-error">${error}</div>
    </c:if>

    <div class="card">
        <form:form modelAttribute="author" method="post" action="/authors">
            <div class="field">
                <label>Name</label>
                <form:input path="name"/>
                <form:errors path="name" cssClass="field-error"/>
            </div>
            <div class="field">
                <label>Email</label>
                <form:input path="email" type="email"/>
                <form:errors path="email" cssClass="field-error"/>
            </div>
            <div class="field">
                <label>Nationality</label>
                <form:input path="nationality"/>
            </div>
            <div class="actions">
                <button type="submit" class="btn">Create Author</button>
                <a href="/authors" class="btn btn-secondary">Cancel</a>
            </div>
        </form:form>
    </div>
</main>
</body>
</html>
