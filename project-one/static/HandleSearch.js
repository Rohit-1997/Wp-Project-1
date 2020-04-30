document.addEventListener('DOMContentLoaded', () => {
    var isbn = "";
    document.querySelector('#error').innerHTML =''
    document.querySelector('#wrapper-2').style.display = 'none'
    document.querySelector("#search-form").onsubmit = () => {
        
        // initializing a new request
        console.log("In form submit");
        const request = new XMLHttpRequest();
        let isbn = document.querySelector("#search-input").value;
        request.open('POST', '/api/search');

        // Creating a callback onload function
        // This gets called if the request initialized gets a successful response
        request.onload = () => {
            document.querySelector('#error').innerHTML =''
            document.querySelector('#block').style.display = 'block';
            document.querySelector('#wrapper').style.display = 'none'
            document.querySelector('#wrapper-1').style.display = 'none'
            document.querySelector('#wrapper-2').style.display = 'none'
            // Get the json data
            const data = JSON.parse(request.responseText);
            const mainList = document.querySelector("#result-area");
            mainList.innerHTML = "";
            console.log(data);
            
    //         // update the result area
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

    //     // adding the data to form so the python function can access it
        const data = new FormData();
        data.append('isbn', isbn);
        request.send(data);
        return false;   // To prevent the reload of the page  
    }
    

    document.querySelector("#result-area").onclick = (e) => {
        const request = new XMLHttpRequest();
        request.open('POST', '/api/book_details');
        isbn = e.srcElement.id
        request.send(e.srcElement.id);
        


        request.onload = () => {
            document.querySelector('#error').innerHTML =''
            document.querySelector('#block').style.display = 'none';
            document.querySelector('#wrapper').style.display = 'block'
            document.querySelector('#wrapper-1').style.display = 'block'
            
            // document.querySelector('#block').innerHTML = '';
            const data = JSON.parse(request.responseText);
            console.log(data)
            const div = document.querySelector('#wrapper')
            console.log(div)
            div.innerHTML = `<div class="container bookdetails-section">
                     <div class="row">
                          <div class="col-md-6">
                        <h2 class="text-center">Book Details</h2>
                    <ul class="list-group"><li class="list-group-item"><strong>Book Title: </strong> ${ data.title }</li>
                    <li class="list-group-item"><strong>Book Author:</strong> ${ data.author }</li>
                    <li class="list-group-item"><strong>Book ISBN:</strong> ${ data.isbn }</li>
                     <li class="list-group-item"><strong>Book year:</strong> ${ data.year }</li>
                     </ul>
                      </div>
                    </div>
                  </div>`
            const r = document.querySelector('#section')
            console.log(r)
            
            if (data['reviews'] === 'null'){
                r.innerHTML = `<h4 class="pd-2 mb-2 reviews-header">No reviews to display yet, Please provide a review</h4>`
            } else{
                r.innerHTML ='<h4 class="pd-2 mb-2 reviews-header">Reviews :</h4>'
                arr = data['reviews']
                for (var i = 0; i < arr.length; i++) {
                    r.innerHTML += `<div class="media pd-2">
                      <img class="mr-3" src="/static/default-profile.png" alt="profile image" height="80" width="80">
                      <div class="media-body pb-2">
                        <h5 class="mt-0">${ arr[i]['username'] }</h5>
                        <h6 class="mt-0"><strong>Rating: </strong> ${ arr[i]['rating']}</h6>
                        ${ arr[i]['review']}
                      </div>
                    </div>`
                }
            }
             document.querySelector('#wrapper-2').style.display = 'block'
        } 

        return false

    }

    document.querySelector("#reviewform").onsubmit = () => {
        const request = new XMLHttpRequest();
        msg = document.querySelector("#reviewpost").value
        rat = document.querySelector("#rating").value
        console.log(request,typeof request)
        // console.log(msg,rat)
        request.open('POST', '/api/submit_review');

        request.onload = () => {
        console.log(msg,rat)
            const d = JSON.parse(request.responseText);
            if (d.success){
                console.log(d)
                const r = document.querySelector('#section')
                r.innerHTML += `<div class="media pd-2">
                      <img class="mr-3" src="/static/default-profile.png" alt="profile image" height="80" width="80">
                      <div class="media-body pb-2">
                        <h5 class="mt-0">${ d['user'] }</h5>
                        <h6 class="mt-0"><strong>Rating: </strong> ${ rat}</h6>
                        ${ msg }
                      </div>
                    </div>`
               
            }else{
               let error = document.querySelector('#error')
               error.innerHTML = d['statement']
            }
            document.querySelector("#reviewpost").value = ''
            document.querySelector("#rating").value = '0'
        }
        const data = new FormData()
        data.append('post-review-data', msg);
        data.append('rating-value', rat);
        data.append('isbn',isbn)
        request.send(data);

        return false   
    }
    document.querySelector("#reviewpost").onfocus = () => {
        document.querySelector('#error').innerHTML =''
    }
    document.querySelector("#rating").onfocus = () => {
        document.querySelector('#error').innerHTML =''
    }
})

