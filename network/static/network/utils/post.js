// Posts a post 
function post() {
    let csrftoken = getCookie('csrftoken');

    let headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);

    fetch('/posts', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            content: document.querySelector('.textarea').value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(response.status);
        }
        return response.json()
    })
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error(error)
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export {post, getCookie};