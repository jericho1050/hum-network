import { post } from './utils/post.js';
import { follow } from './utils/follow.js';
import { edit } from './utils/edit.js';
import { like } from './utils/like.js';
import { animateHeartIcon } from './utils/animateHeart.js';




document.addEventListener('DOMContentLoaded', () => {


    // POST request/ Post a post 
    const postForm = document.querySelector('#post-form');
    if (postForm != null) {
        postForm.addEventListener('submit', () => post())
    }

    // POST request/ follows or unfollows a user
    const followForm = document.querySelector('#follow-form');
    if (followForm != null) {
        document.querySelector('#follow-form').addEventListener('submit', () => follow())
    }

    // when clicked edit the content showing a textarea
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className == 'far fa-edit') {
            let postId = element.dataset.post;
            let contentElement = document.querySelector(`#content-${postId}`);
            let currentContent = contentElement.textContent;

            // check to prevent button text to be appended in textarea
            if (!document.querySelector(`#save-button-${postId}`)) {
                contentElement.innerHTML = `
            <textarea class="col-12">${currentContent}</textarea>
            <button id="save-button-${postId}" type="submit" class="btn btn-primary btn-sm">Save</button>
            <button id="cancel-button-${postId}" type="submit" class="btn btn-danger btn-sm">Cancel</button>
            `;

                const content = document.querySelector(`#content-${postId} textarea`);

                // POST / save newly content 
                document.querySelector(`#save-button-${postId}`).onclick = () => {
                    edit(content.value, postId);
                    contentElement.innerHTML = `${content.value}`;
                    contentElement.dataset.content = `${content.value}`;
                };

            }
            // cancel editing process
        } else if (element.id.startsWith('cancel-button-')) {
            let postId = element.id.split('-')[2];
            let contentElement = document.querySelector(`#content-${postId}`);
            let originalContent = contentElement.dataset.content;
            contentElement.innerHTML = originalContent;
        }
    })

    // when heart icon is clicked 
    document.addEventListener('click', event => {
        const element = event.target;
        console.log(element);

        // checks wether its the svg or img heart icon
        if (element.tagName === "svg" || element.className === "heart-animation") {
            const postId = element.parentElement.id.split('-')[1];

            // unlikes a post 
            if (element.getAttribute("liked") === 'true') {
                let count = parseInt(document.getElementById(`like-count-${postId}`).innerHTML);
                count -= 1;
                document.querySelector(`#like-count-${postId}`).innerHTML = count;
                const heartImg = document.querySelector(`#heart-icon-${postId}`);
                console.log(heartImg);
                heartImg.remove();
                const heartIcon = document.querySelector(`#react-${postId}`);
                heartIcon.firstElementChild.style.display = 'inline-block';
                console.log(heartIcon);
                like(postId, 'unlike');
            }
            // likes a post
            else {
                let count = parseInt(document.getElementById(`like-count-${postId}`).innerHTML);
                count += 1;
                document.querySelector(`#like-count-${postId}`).innerHTML = count;
                like(postId, 'like');
                element.style.display = 'none';

                // replaces outline heart icon
                animateHeartIcon(element, postId);
            }

        }
    })



});



