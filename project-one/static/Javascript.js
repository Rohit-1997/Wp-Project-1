document.addEventListener('DOMContentLoaded', () => {
    var isbn = "";
    document.querySelector("#API-search-form").onsubmit = () => {

        console.log("search form is printing")
        const request = new XMLHttpRequest();
        let isbn = document.querySelector("#search-input").value;
        request.open('POST' ,'/api/search/isbn');

        request.onload = () => {


            const search_result = JSON.parse(request.responseText);
            const mainlist = document.querySelector("#result-area")
            mainlist.innerHTML = "";
            console.log(search_result);


            if(search_result.success){
                const books = search_result.books;
            
                console.log(books)
                books.map((book) => {
                    let content = `Book Title: ${book.title}, Books ISBN: ${book.isbn}`;
                    let link_item = document.createElement("a");
                    let list_item = document.createElement("li");
                    list_item.setAttribute("class", "list-group-item");
                    link_item.setAttribute("id", `${book.isbn}`);
                    link_item.setAttribute("href", "");
                    link_item.innerHTML = content;
                    list_item.append(link_item);
                    mainlist.appendChild(list_item);
                })        
            }
            else{
                let invalid_msg = document.createElement("h3");
                invalid_msg.setAttribute("class", "text-center");
                invalid_msg.innerHTML = "Sorry, Please enter vaild isbn number";
                document.querySelector('#result-area').appendChild(invalid_msg);
            }
        }


        const searchresult = new FormData();
        searchresult.append('isbn', isbn);
        request.send(searchresult);
        return false;   
    }
})