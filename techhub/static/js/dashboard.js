// Example: Handle form submission using AJAX
$(document).ready(function () {
    $('#new-post-form').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/create_post',
            data: new FormData(this),
            contentType: false,
            processData: false,
            success: function (response) {
                // Handle success (e.g., show a success message)
            },
            error: function (error) {
                // Handle errors (e.g., show an error message)
            }
        });
    });
});
