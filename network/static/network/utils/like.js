export function like(post_id, action) {
    fetch(`/like/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            post_id: post_id,
            action: action
        })
    })
    .then(response => {
        if(!response.ok) {
            throw new Error(response.status);
        }
        return response.json();
    })
    .then(result => console.log(result))
}