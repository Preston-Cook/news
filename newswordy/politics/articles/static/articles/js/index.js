document.addEventListener("DOMContentLoaded", () => {

    // Set Register as active on navbar
    document.querySelector('#trending-link').setAttribute('class', 'nav-link active')

    document.querySelectorAll('.save.btn.btn-primary').forEach((elm) => {
        elm.onclick = () => {

            // Log Inner HTML to console
            const text = elm.innerHTML;
            
            // Retrieve parent from node
            const parent = elm.parentNode;

            // Retrieve article info from parent
            const title = parent.querySelector('.card-title').innerHTML;
            const content = parent.querySelector('.card-text').innerHTML;
            const url = parent.querySelector('.article-link.btn.btn-primary').getAttribute('href');
            const img = parent.querySelector('.card-img-top').getAttribute('src');
            const publication_date = parent.querySelector('span').innerHTML;

            if (text === 'Save Article') {

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
                elm.innerHTML = 'Unsave Article'
            }
            else {

                // Call custom API route to delete post from database
                fetch('/delete/', {
                    method: 'PUT',
                    body: JSON.stringify({
                        title: title,
                        content: content, 
                        url: url, 
                        img: img,
                        publication_date: publication_date
                    })
                })
                elm.innerHTML = 'Save Article'
            }
        }
    })
})