$(document).ready(function(){
    $("#id_type").change(function(){
        if($(this).val() !== ""){
            $.ajax({
                url: "/api/project/type/" + $(this).val(),
                type: 'GET',
                cache: false,
                success: function(result) {
                    //  alert(jQuery.dataType);
                    if (result) {
                        console.log(result.title);
                        //  var dd = JSON.parse(result);
                        $(".model-project .form-row").each(function(index,element){
                            if( index >= 9+(parseInt(result.marahel_count)*3 )){
                                // console.log(index+": "+$(this).text());
                                $(this).fadeOut();
                            }
                            //alert($(this).text())
                        });
                    }

                },
                error: function() {
                    alert("No");
                }
            });
        }
    });

});