$(document).ready(function(){

    $("#id_type").change(function(){
        update_data_ptype($(this));
    });


    function update_data_ptype(elem){

        if(elem.val() !== ""){
            $.ajax({
                url: "/api/project/type/" + elem.val(),
                type: 'GET',
                cache: true,
                success: function(result) {
                    if (result) {
                        console.log(result.title);
                        //  var dd = JSON.parse(result);
                        $(".model-project .form-row").each(function(index,element){
                            if(index >= 9 && index % 3 === 0){
                                console.log(index / 3 - 3);
                                if($(this).find("label").attr("first_run") === "false"){
                                    $(this).find("label").text(result.marahel[(index / 3 - 3)]);
                                    $(this).find("label").css({"width": "100%"});
                                }else{
                                    $(this).find("label").text($(this).find("label").text()+" | "+result.marahel[(index / 3 - 3)]);
                                    $(this).find("label").css({"width": "100%"});
                                }
                                $(this).find("label").attr("first_run", "false");
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
    }

    update_data_ptype($("#id_type"));

});