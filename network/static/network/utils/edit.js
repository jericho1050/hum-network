export function edit(content, postId) {

    let csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];

    fetch('/posts', {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: content,
            post_id: postId
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
    .catch(error => console.log(error)).catch(error => console.error(error))
}
