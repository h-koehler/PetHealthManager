$(document).ready(function() {
    $('button#pets-tab').click(function() {
        const username = $(this).attr('data-username')
        const ajax_url = $(this).attr('data-ajax-url')

        $.ajax({
            url: ajax_url,
            type: "GET",
            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (html) {
                $('#profile-details').hide();
                $('#user-pets').html(html).show()

                $('.primary-button').removeClass('active')
                $('#pets-tab').addClass('active')
            })
            .fail(function(xhr, status, error) {
                console.error("Failed to load updates:", error)
            })
    })

    $('button#profile-tab').click(function() {
        $('#user-pets').hide();
        $('#profile-details').show();

        $('.primary-button').removeClass('active');
        $('#profile-tab').addClass('active');
    })
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');