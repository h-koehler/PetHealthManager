$(document).ready(function() {
    $('button#updates-tab').click(function() {
        const petId = $(this).attr('data-pet-id')
        const ajax_url = $(this).attr('data-ajax-url')

        $.ajax({
            url: ajax_url,
            data: {
                pet_id: petId
            },
            type: "GET",
            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function (html) {
                $('#main-container').hide();
                $('#updates-content').html(html).show()

                $('.primary-button').removeClass('active')
                $('#updates-tab').addClass('active')
            })
            .fail(function(xhr, status, error) {
                console.error("Failed to load updates:", error)
            })
    })

    $('button#profile-tab').click(function() {
        $('#updates-content').hide();
        $('#main-container').show();

        $('.primary-button').removeClass('active');
        $('#profile-tab').addClass('active');
    })
})