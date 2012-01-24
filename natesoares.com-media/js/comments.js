$(document).ready(function() {
    var name, site, comment;
    $('#comments form').ajaxForm({
        beforeSubmit: function(data) {
            name = site = content = false;
            for(var i in data) {
                if(data[i].name == 'name') name = data[i].value;
                if(data[i].name == 'url') site = data[i].value;
                if(data[i].name == 'comment') content = data[i].value;
            }
        },
        success: function() {
            var head = site? ('<a href="'+site+'" title="Website of '+name+'">'+name+'</a>'): name;
            var comment = $('<div class="comment bubble"></div>');
            comment.append($('<div class="name">'+head+' says:</div>'));
            comment.append('<div class="content">'+content+'</div>').hide();
            if($('#comments .comment:last').length)
                $('#comments .comment:last').after(comment);
            else $('#comments .intro').after(comment);
            comment.fadeIn();
			$('#comments form').clearForm();
        },
    });
});
