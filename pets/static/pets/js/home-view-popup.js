$(document).ready(function () {
    $('a.pet-card').click(function () {
        const petId = $(this).attr('data-pet-id')
        const ajax_url = $(this).attr('data-ajax-url')
        console.log("Pet ID before AJAX:", petId);

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                pet_id: petId
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
                 const backdrop = $(`.popup-backdrop[data-popup-id="${petId}"]`);
                 const container = backdrop.find('.popup-container');

                 // conditions
                const conditionList = container.find('.conditions');
                conditionList.empty();
                if (json.conditions.length === 0) {
                    conditionList.append('<li>No conditions listed.</li>');
                } else {
                    json.conditions.forEach(condition => {
                        conditionList.append(`<li><strong>${condition.title}:</strong> ${condition.description}</li>`);
                    });
                }

                // vaccines
                const vaccineList = container.find('.vaccines');
                vaccineList.empty();
                if (json.vaccines.length === 0) {
                    vaccineList.append('<li>No vaccinations listed.</li>');
                } else {
                    json.vaccines.forEach(vaccine => {
                        vaccineList.append(`<li><strong>${vaccine.name}</strong>: Last: ${vaccine.last_done}, Next: ${vaccine.next_due}</li>`);
                    });
                }
                backdrop.removeClass('hidden');
                container.removeClass('hidden');
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                // console.log("Status: " + status);
                // console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function () {
                // alert("The request is complete!");
            });
    })

    // close popup
    $(document).on('click', '.popup-backdrop', function (e) {
        const popup = $(this).find('.popup-content');

        if (!popup.is(e.target) && popup.has(e.target).length === 0) {
            $(this).addClass('hidden')
            popup.addClass('hidden')
        }
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