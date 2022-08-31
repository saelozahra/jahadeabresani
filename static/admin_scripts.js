$(document).ready(function(){
    $("#id_type").change(function(){
        if($(this).val() !== ""){
            $.ajax({
                url: "/api/project/type/" + $(this).val(),
                type: 'GET',
                cache: false,
                success: function(result) {
                    if (result) {
                        console.log(result.title);
                        //  var dd = JSON.parse(result);
                        $(".model-project .form-row").each(function(index,element){
                            if(index >= 9 && index % 3 == 0){
                                console.log(index / 3 - 3);
                                $(this).find("label").text($(this).find("label").text()+" | "+result.marahel[(index / 3 - 3)]);
                                // $(this).css({"color": "red", "background-color": "green"});
                            }
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