/* Closing */

function closer_cookie() {
    var id_string = $.cookie('closed'),
        id_array = id_string? id_string.split(','): [],
        ids = {};
    for(var i in id_array) ids[id_array[i]] = true;

    function record() {
        var id_string = '';
        for(var i in ids) id_string = id_string + (id_string? ',': '') + i;
        $.cookie('closed', id_string);
    };

    this.contains = function(id) { return ids[id]; };
    this.add = function(id) { ids[id] = true; record(); };
    this.remove = function(id) { delete ids[id]; record(); };
};

function toggle_comment(comment) {
    var comments = $('~ .comments', comment),
        close = !comment.is('.closed'),
        editing = comment.is('.editing'),
        action = close? 'hide': 'show';
    try { cancel_reply(comment); } catch(e) { /* New comments have not been enabled. */ }

    /* We need to know whether to hide / show the form.content or the div.content */
    type = editing? 'form': 'div';

    $(type+'.content, .bottom, .edit', comment)[action]();
    $('> .comment', comments)[action]();
    if(close) comment.addClass('closed').find('.close').html('[+]').removeClass('close').addClass('open');
    else comment.removeClass('closed').find('.open').html('[-]').removeClass('open').addClass('close');
};

function close_comment(comment) { close_or_open_comment(comment, true); };
function open_comment(comment) { close_or_open_comment(comment, false); };

const closer = '<a class="smallgrey close">[-]</a>';

$(document).ready(function() {
    var closed = new closer_cookie();

    $('#comments .comment .container').each(function() {
        $('.top .right, .removed .right', this).append(closer);
        if(closed.contains($(this).attr('id'))) toggle_comment($(this));
    });
    $('#comments .close').live('click', function() {
        var comment = $(this).parents('.container');
        toggle_comment(comment);
        closed.add(comment.attr('id'));
    });
    $('#comments .open').live('click', function() {
        var comment = $(this).parents('.container');
        toggle_comment(comment);
        closed.remove(comment.attr('id'));
    });
});


/* Editing */

$(document).ready(function() {
    $('#comments .edit').live('click', function() {
        var comment = $(this).parents('.container');
        $('.content', comment).slideToggle('fast');
        if(comment.is('.editing')) comment.removeClass('editing').find('.edit').html('[edit]');
        else comment.addClass('editing').find('.edit').html('[cancel]');
        return false;
    });
    $('#comments form.content [name=next]').remove();
    $('#comments form.content').each(function() {
        var form = $(this);
        form.ajaxForm(function(r) {
            var comment = form.parents('.container');
            comment.find('div.content').html(r);
            comment.find('.edit').click();
        });
    });
});


/* Login */

$(document).ready(function() {
    $('#login-register').dialog({
        autoOpen: false,
        modal: true,
        resizable: false,
        draggable: false,
        width: '80%',
    });
    $('#comments .login').live('click', function() {
        $('#login-register').dialog('open');
        return false;
    });
});


/* Administration */
$(document).ready(function() {
    $('#comments .staff-aide').each(function() {
        var form = $(this);
        form.ajaxForm(function() {
            var edit = $('.goto-edit', form).clone(true),
                removed = $('<div class="removed"></div>');
            removed.html('(Comment removed) ').append(edit);
            form.parents('.container').html(removed);
        });
    });
});
