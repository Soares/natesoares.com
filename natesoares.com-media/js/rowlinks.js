$(document).ready(function() {
    $('#items tr input').click(function(e) { e.stopPropagation(); });
    $('#items tr').addClass('link').click(function() {
        window.location = $('a', this).attr('href');
    });
});
