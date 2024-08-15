document.addEventListener('DOMContentLoaded', function() {
    // Comment Box Functionality
    const commentIcon = document.getElementById('comment-icon');
    const textBox = document.getElementById('text-box');
    const textArea = document.getElementById('text-area');
    const commentList = document.getElementById('comment-list');
    const tweetId = document.getElementById('tweet-id')?.value; // Ensure tweet-id is available

    if (commentIcon && textBox && textArea && commentList) {
        commentIcon.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link action
            textBox.classList.toggle('hidden');
            textArea.focus(); // Focus on the text area when shown
        });

        textArea.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevent the newline character
        
                const textContent = textArea.value.trim();
                if (textContent) {
                    fetch('/add-comment/', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ tweet_id: tweetId, text: textContent }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.error('Error:', data.error);
                            return;
                        }
        
                        // Append the new comment to the comment list
                        const newComment = document.createElement('div');
                        newComment.classList.add('comment-item');
                        newComment.innerHTML = `
                            <div class="comment-avatar">
                                <a href="/profile/${data.user}">
                                    <img src="${data.avatar_url}" alt="${data.user}" class="rounded-circle" style="width: 50px; height: 50px; object-fit: cover;">
                                </a>
                            </div>
                            <div class="comment-text">
                                <p><strong>${data.user}:</strong> ${data.text}</p>
                            </div>
                        `;
                        commentList.appendChild(newComment);
        
                        // Optionally hide the text box after updating
                        textBox.classList.add('hidden');
                        textArea.value = ''; // Clear the text area
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }
            }
        });
    } else {
        console.error('One or more comment-related elements not found.');
    }

    // Like Button Functionality
    const likeButtons = document.querySelectorAll(".like-btn");
    const dropdownToggleButtons = document.querySelectorAll(".dropdown-toggle");

    likeButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            
            // Disable the button to prevent multiple clicks
            this.classList.add("disabled");
            
            const icon = this.querySelector("i");
            const likeCountSpan = this.nextElementSibling;
            const tweetId = this.getAttribute("data-tweet-id");

            fetch(`/toggle-like/${tweetId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    icon.classList.remove("fa-regular", "fa-heart");
                    icon.classList.add("fa-solid", "fa-heart");
                } else {
                    icon.classList.remove("fa-solid", "fa-heart");
                    icon.classList.add("fa-regular", "fa-heart");
                }
                likeCountSpan.textContent = data.like_count;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            })
            .finally(() => {
                this.classList.remove("disabled");
            });
        });
    });

    // Dropdown Toggle Functionality
    dropdownToggleButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            
            // Toggle the dropdown menu
            const dropdownMenu = this.nextElementSibling;
            const isVisible = dropdownMenu.classList.contains('show');
            
            // Hide all dropdown menus
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('show');
            });
            
            // Toggle the clicked dropdown menu
            if (!isVisible) {
                dropdownMenu.classList.add('show');
            }
        });
    });

    // Close dropdown menu if clicked outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
