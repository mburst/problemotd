$(document).ready(function(){
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
   });
    
    var submitting = false;
    
    $("#subscribe").on('submit', function(event){
        event.preventDefault();
        //Prevent multiple form submissions
        if (submitting) {
            return false;
        }
        submitting = true;
        $("body").css("cursor", "wait");
        $.ajax({
            url: '/subscribe/',
            data: {'email': this.email.value},
            success: function(data){
                alert(data);
                $("#subscribe input").val('');
            },
            error: function(data){
                alert(data.responseText);
            }
        }).done(function(){
            $("body").css("cursor", "");
            submitting = false;
        });
    });
    
    $("#commenters").on("click", ".reply", function(event){
        event.preventDefault();
        var self = $(this).parent();
        if (self.siblings("form").length == 0) {
            var form = $("#postcomment").clone(true);
            form.find("#preview").html('');
            form.find('.ancestor').val(self.parent().attr('id'));
            self.after(form);
        }
    });
    
    $("#postcomment").on('submit', function(e){
        $(this).find("#id_password").val('potd');
    })
    
    $("#shcomments").on('click', function(){
        $("#comments").toggle(1000);
    });
    
    $(".preview").on('click', function(){
        submitting = true;
        
        var parent = $(this).parent().parent();
        
        $.ajax({
            url: '/preview/',
            data: {'text': parent.find("textarea").val()},
            success: function(data){
                parent.find("#preview").show();
                parent.find("#preview").html(data);
                parent.find("#preview pre code").each(function(i, e) {hljs.highlightBlock(e)});
            },
            error: function(data){
                alert(data.responseText);
            }
        }).done(function(){
            $("body").css("cursor", "");
            submitting = false;
        });
    });
    
    $(".delete").on('click', function(e){
        e.preventDefault();
        
        if (confirm('Are you sure you want to delete this comment?')) {
            submitting = true;
            
            var parent = $(this).parent().parent();
            
            $.ajax({
                url: $(this).attr('href'),
                type: 'POST',
                success: function(data){
                    if (data == 'removed') {
                        parent.hide('slow', function(){ parent.remove(); });
                    } else {
                        parent.html("[Deleted]<p>This comment was removed</p>");
                    }
                },
                error: function(data){
                    alert(data.responseText);
                }
            }).done(function(){
                $("body").css("cursor", "");
                submitting = false;
            });
        }
    });
});