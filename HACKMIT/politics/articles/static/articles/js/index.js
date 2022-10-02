document.addEventListener("DOMContentLoaded", () => {

    // Set active class on class item
    document.querySelector('#trending-link').setAttribute('class', 'nav-link active');

    // Add event listeners to save article buttons
    document.querySelectorAll('.save.btn.btn-primary').forEach((elm) => {
        elm.onclick = () => {

            // Retrieve parent from node
            const parent = elm.parentNode;

            // Retrieve article info from parent
            const title = parent.querySelector('.card-title').innerHTML;
            const content = parent.querySelector('.card-text').innerHTML;
            const url = parent.querySelector('.article-link.btn.btn-primary').innerHTML;
            const img = parent.querySelector('.card-img-top').innerHTML;
            const publication_date = parent.querySelector('span').innerHTML;

            // Call custom API route and save post to database and link
            fetch('/save/', {
                method: "PUT",
                body: JSON.stringify({
                    title: title,
                    content: content, 
                    url: url,
                    img: img,
                    publication_date: publication_date
                })
            })

            
        }
    })
})

