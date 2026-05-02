<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title>SGA Library</title>
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
    <div class="card">
        <h2>Welcome</h2>
        <p>This Spring Boot application manages <strong>Authors</strong> and their <strong>Books</strong> with a One-to-Many relationship.</p>
        <p>Use the navigation above to browse, create, and update records.</p>
        <ul>
            <li><a href="/authors">View Authors</a></li>
            <li><a href="/books">View Books</a></li>
            <li><a href="/books/with-authors">Books joined with Authors (custom inner-join query)</a></li>
        </ul>
    </div>
</main>
</body>
</html>
