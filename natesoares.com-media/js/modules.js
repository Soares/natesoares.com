$.fn.extend({
    closable: function() {
        this.each(function() {
            $('a', this).click(function(e) { e.stopPropagation(); });
            var id = $(this).attr('id');

            if($.cookie(id)) {
                $(this).addClass('closed');
                $('.opener', this).html('&#x25B8 ');
            } else {
                $('.opener', this).html('&#x25BE ');
            }

            $(this).click(function() {
                if($(this).is('.closed')) {
                    $('.body', this).slideDown();
                    $('.opener', this).html('&#x25BE ');
                    $.cookie(id, null, {path: '/', expires: -1});
                    $(this).removeClass('closed');
                } else {
                    $('.body', this).slideUp();
                    $('.opener', this).html('&#x25B8 ');
                    $.cookie(id, true, {path: '/', expires: 8});
                    $(this).addClass('closed');
                }
            });
        });
    },
});

$(document).ready(function() {
    $('#right .closable.module').closable();
});
