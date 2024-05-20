$(document).ready(function() {
    // Make/Remove moderator button click event
    $(document).on('click', '.add-manager', function() {
        var userId = $(this).data('user-id');
        makeRemoveManager(userId, 'add');
    });

    $(document).on('click', '.remove-manager', function() {
        var userId = $(this).data('user-id');
        makeRemoveManager(userId, 'remove');
    });
});

function makeRemoveManager(userId, action) {
    $.ajax({
        url: '/community/make_remove_manager/',
        method: 'POST',
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        data: {
            community_id: communityId,
            user_id: userId,
            action: action
        },
        success: function(response) {
            location.reload();
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(xhr.responseText);
        }
    });
}

function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    return cookieValue;
}