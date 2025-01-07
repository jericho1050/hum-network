import { S3_URL } from './config.js';

export function animateHeartIcon(svgElement, postId) {
    // Get the wrapper element containing the SVG
    const svgWrapper = svgElement.parentElement;
  
    // Insert red heart icon into the wrapper
    const heartIcon = document.createElement('img');
    heartIcon.src = `${S3_URL}/heart.png`;
    svgWrapper.appendChild(heartIcon);
  
    heartIcon.classList.add('heart-animation');
    heartIcon.setAttribute('id', `heart-icon-${postId}`);
    heartIcon.setAttribute('liked', 'true')
  
    // remove the original SVG after animation completes
    // svgElement.parentElement.addEventListener('animationend', () => {
    //   svgElement.style.display = 'none';
    // });
  }
  