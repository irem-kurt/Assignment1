$(document).ready(function() {

    $('.map').each(function() {
        // Extract post ID and index from map ID
        console.log($(this).attr('id'));
        var ids = $(this).attr('id').split('-');
        var postId = ids[1];
        var index = ids[2];
        console.log(postId);
        console.log(index);
        // Get location coordinates from data attribute
        var location = $(this).data('location');
        var latitude = parseFloat(location.split(',')[0]);
        var longitude = parseFloat(location.split(',')[1]);
        console.log(location);
        console.log(latitude);
        console.log(longitude);

        // Initialize Leaflet map
        console.log('map-' + postId + '-' + index);
        var map = L.map('map-' + postId + '-' + index).setView([latitude, longitude], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add marker to map
        L.marker([latitude, longitude]).addTo(map);
    });

    // Add event listener for like buttons
    $('.like-btn').click(function() {
        var postId = $(this).data('post-id');
        handleLikeDislike(postId, 'like');
    });

    // Add event listener for dislike buttons
    $('.dislike-btn').click(function() {
        var postId = $(this).data('post-id');
        handleLikeDislike(postId, 'dislike');
    });

    submitComment();

    followRequests();
});

function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    return cookieValue;
}

function handleLikeDislike(postId, action) {
    // Send a POST request to the server with postId and action
    $.ajax({
        type: "POST",
        url: "/post/like_dislike/",
        data: {
            'post_id': postId,
            'action': action,
        },
        headers: {
            "X-CSRFToken": getCSRFToken() // Include CSRF token in the headers
        },
        dataType: 'json',
        success: function(response) {
            // Check if the action was successful
            if (response.success) {
                // Reload the page to reflect the changes
                location.reload();
            } else {
                // Handle the error if needed
                console.log('Error:', response.message);
            }
        },
        error: function(xhr, errmsg, err) {
            // Handle any errors that occur during the request
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
}

function submitComment() {
    // Handle submit comment button click
    $('.submit-comment-btn').on('click', function() {
        // Get the post ID from the data attribute
        const postId = $(this).data('post-id');
        // Get the comment text from the input field using the corresponding post ID
        const commentText = $('#comment-text-' + postId).val().trim();

        // Check if comment text is empty
        if (commentText === '') {
            alert('Please enter a comment.');
            return;
        }

        // Construct AJAX request
        $.ajax({
            url: "/post/add_comment/",
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken() // Include CSRF token in the headers
            },
            data: {
                post_id: postId,
                text: commentText
            },
            success: function(data) {
                // Handle success response
                console.log(data);
                // Reload the page to update comments (you can modify this according to your needs)
                location.reload();
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error(xhr.responseText);
            }
        });
    });
}

function followRequests() {
    // AJAX for joining community
    $('.join-btn').click(function() {
        var communityId = $(this).data('community-id');
        $.ajax({
            url: '/community/join/',
            method: 'POST',
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            data: {
                community_id: communityId,
            },
            success: function(response) {
                location.reload();
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error(xhr.responseText);
            }
        });
    });

    // AJAX for quitting community
    $('.quit-btn').click(function() {
        var communityId = $(this).data('community-id');
        $.ajax({
            url: '/community/quit/',
            method: 'POST',
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            data: {
                community_id: communityId,
            },
            success: function(response) {
                location.reload();
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error(xhr.responseText);
            }
        });
    });

    // AJAX for sending request to join community
    $('.send-request-btn').click(function() {
        var communityId = $(this).data('community-id');
        console.log('send request to join community with id: ' + communityId);
        $.ajax({
            url: '/community/request/',
            method: 'POST',
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            data: {
                community_id: communityId,
            },
            success: function(response) {
                console.log('send request success ' + communityId);
                location.reload();
            },
            error: function(xhr, status, error) {
                console.log('send request error ' + communityId + ' ' + xhr.responseText);
                // Handle error
                console.error(xhr.responseText);
            }
        });
    });
}
