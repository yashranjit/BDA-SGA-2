<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %> <%@ taglib
prefix="form" uri="http://www.springframework.org/tags/form" %>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Book Form</title>
        <style>
            body {
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                margin: 40px;
                background-color: #f8f9fa;
                color: #333;
            }
            .container {
                max-width: 500px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }
            input[type="text"],
            select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .btn-save {
                padding: 10px 20px;
                background-color: #198754;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 4px;
                font-size: 16px;
            }
            .btn-save:hover {
                background-color: #157347;
            }
            .cancel-link {
                margin-left: 15px;
                color: #dc3545;
                text-decoration: none;
            }
            .error-msg {
                color: #842029;
                background-color: #f8d7da;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Dynamic header depending on whether we have an ID (Update) or not (Create) -->
            <h2>${empty book.id ? 'Add New' : 'Update'} Book</h2>

            <!-- Displays the DataIntegrityViolationException message if validation fails -->
            <c:if test="${not empty error}">
                <div class="error-msg">${error}</div>
            </c:if>

            <!-- Spring form binding to our 'book' model attribute -->
            <form:form action="/books/save" modelAttribute="book" method="POST">
                <!-- Hidden field to keep track of the ID during updates -->
                <form:hidden path="id" />

                <div class="form-group">
                    <label>Title:</label>
                    <!-- path="title" directly binds to the setTitle() method in our Java class -->
                    <form:input
                        path="title"
                        required="required"
                        placeholder="Enter book title"
                    />
                </div>

                <div class="form-group">
                    <label>Genre:</label>
                    <form:input
                        path="genre"
                        required="required"
                        placeholder="Enter genre"
                    />
                </div>

                <div class="form-group">
                    <label>Author:</label>
                    <!-- Binding the selected author ID to the book's author property -->
                    <form:select path="author.id">
                        <form:option value="" label="-- Select an Author --" />
                        <c:forEach var="auth" items="${authors}">
                            <form:option value="${auth.id}"
                                >${auth.name}</form:option
                            >
                        </c:forEach>
                    </form:select>
                </div>

                <button type="submit" class="btn-save">Save Book</button>
                <a href="/books" class="cancel-link">Cancel</a>
            </form:form>
        </div>
    </body>
</html>
