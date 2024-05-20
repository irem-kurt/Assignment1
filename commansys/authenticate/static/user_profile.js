$(document).ready(function() {
    // Make/Remove moderator button click event
    $(document).on('click', '.follow', function() {
        var userId = $(this).data('user-id');
        console.log(userId);
        followUnfollow(userId, 'follow');
    });

    $(document).on('click', '.unfollow', function() {
        var userId = $(this).data('user-id');
        followUnfollow(userId, 'unfollow');
    });
});

function followUnfollow(userId, action) {
    console.log('followUnfollow' + userId + ' ' + action);
    $.ajax({
        url: '/user/follow_unfollow/',
        method: 'POST',
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        data: {
            user_id: userId,
            action: action
        },
        success: function(response) {
            console.log(user_id);
            window.location.href = '/authenticate/profile/' + user_id + '/';
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error('irem' + xhr.responseText);
        }
    });
}

function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    return cookieValue;
}