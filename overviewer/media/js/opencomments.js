function cancel_reply(comment) {
    $('+ .add', comment).hide();
    $('.cancel', comment).html('[reply]').removeClass('cancel').addClass('reply');
};

function begin_reply(comment) {
    if($('+ .add', comment).length) {
        $('+ .add', comment).show();
        $('.reply', comment).html('[cancel]').removeClass('reply').addClass('cancel');
    } else {
        var id = comment.attr('id').split('-')[1];
        $.ajax({
            url: '/comments/form/'+id+'/',
            success: function(r) {
                var add = $(r);
                add.find('.post').click(function() {
                    $(this).parents('.add').slideUp();
                    comment.siblings('.comments').prepend('<div class="loading">One moment please...</div>');
                });
                add.find('form').ajaxForm(function(r) {
                    var newcomment = $(r);
                    newcomment.hide();
                    comment.siblings('.comments').find('.loading').remove();
                    comment.siblings('.comments').prepend(newcomment);
                    newcomment.fadeIn();
                    cancel_reply(comment);
                });
                comment.after(add);
                begin_reply(comment);
            },
        });
    }
};

$(document).ready(function() {
    $('#comment-adder .add [name=next]').val('/comments/new/');
    $('#comment-adder .add form').ajaxForm(function(r) {
        var newcomment = $(r);
        newcomment.hide();
        $('#comments .count ~ .comments').prepend(newcomment);
        newcomment.fadeIn();
        $('#comment-adder').hide();
        $('#main-add.canceler').html('Add your own').removeClass('canceler').addClass('replier');
    });
    $('#main-add.replier').live('click', function() {
        $('#comment-adder').show();
        $(this).html('Cancel').removeClass('replier').addClass('canceler');
        return false;
    });
    $('#main-add.canceler').live('click', function() {
        $('#comment-adder').hide();
        $(this).html('Add your own').removeClass('canceler').addClass('replier');
        return false;
    });
    $('#comments .reply').live('click', function() {
        begin_reply($(this).parents('.container'));
        return false;
    });
    $('#comments .cancel').live('click', function() {
        cancel_reply($(this).parents('.container'));
        return false;
    });
});
