document.addEventListener('DOMContentLoaded', () => {
    var isbn = "";
    document.querySelector("#search-form").onsubmit = () => {
        // initializing a new request
        console.log("In form submit");
        const request = new XMLHttpRequest();
        isbn = document.querySelector("#search-input").value;
        request.open('POST', '/api/search');

        // Creating a callback onload function
        // This gets called if the request initialized gets a successful response
        request.onload = () => {
            // Get the json data
            const data = JSON.parse(request.responseText);
            const mainList = document.querySelector("#result-area");
            mainList.innerHTML = "";
            console.log(data);
            
            // update the result area
            if (data.success) {
                const books = data.books;
                let contents = "";
                console.log(books)
                books.map((book) => {
                    let content = `Book Title: ${book.title}, Books ISBN: ${book.isbn}`;
                    let list_item = document.createElement("li");
                    let link_item = document.createElement("a");
                    list_item.setAttribute("class", "list-group-item");
                    link_item.setAttribute("id", `${book.isbn}`);
                    link_item.setAttribute("href", "");
                    link_item.innerHTML = content;
                    list_item.append(link_item);
                    mainList.appendChild(list_item);
                })
            } else {
                let header = document.createElement("h3");
                header.setAttribute("class", "text-center");
                header.innerHTML = "Sorry, There are no books with this isbn or you have entered invalid isbn";
                document.querySelector('#result-area').appendChild(header);
            }
        }

        // adding the data to form so the python function can access it
        const data = new FormData();
        data.append('isbn', isbn);
        request.send(data);
        return false;   // To prevent the reload of the page
    }

    document.querySelector("#result-area").onclick = () => {
        const request = new XMLHttpRequest();
        request.open('POST', '/api/book_details');
        request.send(isbn);
    }
})