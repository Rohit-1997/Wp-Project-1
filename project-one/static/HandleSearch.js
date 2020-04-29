document.addEventListener('DOMContentLoaded', () => {
    console.log("In JS");
    document.querySelector("#search-form").onsubmit = () => {
        // initializing a new request
        console.log("In form submit");
        const request = new XMLHttpRequest();
        const isbn = document.querySelector("#search-input").value;
        request.open('POST', '/api/search');

        // Creating a callback onload function
        // This gets called if the request initialized gets a successful response
        request.onload = () => {
            // Get the json data
            const data = JSON.parse(request.responseText);
            console.log(data);
            
            // update the result area
            if (data.success) {
                const contents = `The title of the book is: ${data.title}, The rating is: ${data.average_score}`;
                document.querySelector("#result-area").innerHTML = contents;
            } else {
                document.querySelector('#result-area').innerHTML = "There was some error";
            }
        }

        // adding the data to form so the python function can access it
        const data = new FormData();
        data.append('isbn', isbn);
        request.send(data);
        return false;   // To prevent the reload of the page
    }
})