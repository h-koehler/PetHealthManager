$(document).ready(function () {
    $('button.edit-comment').click(function () {
        const commentId = $(this).attr('data-comment-id');
        const ajaxUrl = $(this).attr('data-ajax-url');
        console.log("Sending GET for comment ID:", commentId);

        $.ajax({
            url: ajaxUrl,
            data: {
                comment_id: commentId
            },
            type: "GET",
            dataType: "json",
            headers: {'X-CSRFToken': csrftoken},
        })
        .done(function (json) {
            console.log(json)
            const container = $(`.comment[data-container-id="${commentId}"]`);
            const oldContent = container.find('.comment-content').text(); // Save old content

            container.find('.comment-content').replaceWith(`
                <form class="edit-comment-form" data-comment-id="${commentId}">
                    <textarea name="content">${json.content}</textarea>
                    <button type="submit">Save</button>
                    <button type="button" class="cancel-edit-comment">Cancel</button>
                    <input type="hidden" name="original" value="${oldContent}">
                </form>
            `);
        })
        .fail(function () {
            alert("Failed to load comment for editing.");
        });
    });

    $(document).on('submit', '.edit-comment-form', function(e){
        e.preventDefault();
        const form = $(this);
        const ajaxUrl = $('button.edit-comment').attr('data-ajax-url');
        const commentId = form.data('comment-id');
        const newContent = form.find('textarea[name="content"]').val();

        $.ajax({
            url: ajaxUrl,
            type: "POST",
            data: {
                comment_id: commentId,
                content: newContent,
            },
            datatype: "json",
            headers: {'X-CSRFToken': csrftoken},
        })
        .done(function(json) {
            form.replaceWith(`<div class="comment-content">${json.content}</div>`);
        })
        .fail(function () {
            alert("Failed to update comment.");
        });
    });

    $(document).on('click', '.cancel-edit-comment', function () {
        const form = $(this).closest('form');
        const originalContent = form.find('input[name="original"]').val();
        form.replaceWith(`<div class="comment-content">${originalContent}</div>`);
    });
});
