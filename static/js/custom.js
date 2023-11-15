$("#add-book").click(function() {
    var addButton = document.getElementById("add-book");
    if ($("#add-div").css("display") === "none") {
        addButton.textContent = "X";
        $("#add-div").slideDown();
    } else {
        addButton.textContent = "Add Book";
        $("#add-div").slideUp();
        $("#add-div").css("display", "none");
    }
    
});

$("#edit-book").click(function() {
    var addButton = document.getElementById("edit-book");
    if ($("#edit-div").css("display") === "none") {
        addButton.textContent = "X";
        $("#edit-div").slideDown();
    } else {
        addButton.textContent = "Edit Book";
        $("#edit-div").slideUp();
        $("#edit-div").css("display", "none");
    }
});

$("#filter-book").click(function() {
    var filterButton = document.getElementById("filter-book");
    if ($("#filter-div").css("display") === "none") {
        filterButton.textContent = "X";
        $("#filter-div").slideDown();
    } else {
        filterButton.textContent = "Filter Book";
        $("#filter-div").slideUp();
        $("#filter-div").css("display", "none");
    }
    
});

function changeOrder() {
    const orderSelect = document.getElementById('orderSelect');
    const selectedOrder = orderSelect.value;

    fetch('/update_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify({ order: selectedOrder })
    })
    .then(response => response.json())
    .then(data => {
        let booksObject = data['books'];
        console.log(booksObject)
        let titles = document.getElementsByClassName('card-title');
        let authors = document.getElementsByClassName('card-author');
        let ratings = document.getElementsByClassName('card-rating');
        let prices = document.getElementsByClassName('card-price');
        let links = document.getElementsByClassName('card-link');
        let images = document.getElementsByClassName('card-img-book')

        for (i=0; i < booksObject.length; i++){

            images[i].src = booksObject[i].coverImg
            titles[i].textContent = booksObject[i].title
            authors[i].textContent = booksObject[i].author
            ratings[i].textContent = booksObject[i].rating
            prices[i].textContent = booksObject[i].price
            links[i].href = "/book_"+ booksObject[i].bookId
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}