$(document).ready(function() {
    // Function to handle accepting a user request
    $(".accept-request").click(function() {
        var userId = $(this).data("user-id");
        $.ajax({
            url: "/community/response/",
            method: 'POST',
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            data: {
                community_id: communityId,
                user_id: userId,
                accept: true,
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

    // Function to handle rejecting a user request
    $(".reject-request").click(function() {
        var userId = $(this).data("user-id");
        $.ajax({
            url: "/community/response/",
            method: 'POST',
            headers: {
                "X-CSRFToken": getCSRFToken()
            },
            data: {
                community_id: communityId,
                user_id: userId,
                accept: false,
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
});

function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    return cookieValue;
}