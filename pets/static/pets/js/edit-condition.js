$(document).ready(function () {
    $('button.edit-condition').click(function () {
        const conditionId = $(this).attr('data-condition-id')
        const ajax_url = $(this).attr('data-ajax-url')
        console.log("Condition ID before AJAX:", conditionId);

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                condition_id: conditionId
            },

            // Whether this is a POST or GET request
            type: "GET",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                const container = $(`.condition-container[data-container-id="${conditionId}"]`);
                const oldDescription = container.find('p').text(); // incase the user selects cancel
                container.find('p').replaceWith(`
                <form class="edit-condition-form" data-condition-id="${conditionId}">
                    <textarea name="description">${json.description}</textarea>
                    <button type="submit">Save</button>
                    <button type="button" class="cancel-edit">Cancel</button>
                    <input type="hidden" name="original" value="${oldDescription}">
                </form>
                `);
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                // console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function () {
                // alert("The request is complete!");
            });
    })

    // save changes to description and close textarea
    $(document).on('submit', '.edit-condition-form', function(e){
        e.preventDefault();
        const ajax_url = $('button.edit-condition').attr('data-ajax-url')
        const form = $(this);
        const conditionId = form.data('condition-id')
        const newDescription = form.find('textarea[name="description"]').val()

        $.ajax({
            url: ajax_url,
            type: "POST",
            data: {
                condition_id: conditionId,
                description: newDescription,
            },
            datatype: "json",
            headers: {'X-CSRFToken': csrftoken},
        })
            .done(function(json) {
                form.replaceWith(`<p>${json.description}</p>`)
            })
            .fail(function () {
                // alert("Failed to update condition description.")
            })
    })

    $(document).on('click', '.cancel-edit', function () {
        const form = $(this).closest('form');
        const originalText = form.find('input[name="original"]').val();
        form.replaceWith(`<p>${originalText}</p>`);
    });


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