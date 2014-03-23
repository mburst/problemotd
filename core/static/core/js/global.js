$(document).ready(function(){
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
            form.find('.ancestor').val(self.parent().attr('id'));
            self.after(form);
        }
    });
    
    $("#shcomments").on('click', function(){
        $("#comments").toggle(1000);
    })
});