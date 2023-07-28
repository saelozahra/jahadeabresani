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
                        $(".model-project .marahel .form-row").each(function(index,element){
                            let index_num = index / 3
                            if(index % 3 === 0){
                                console.log("i:", index, "salam", index/3)
                                console.log(index_num);
                                if($(this).find("label").attr("first_run") === "false"){
                                    $(this).find("label").text(result.marahel[(index_num)]);
                                    $(this).find("label").css({"width": "100%"});
                                }else{
                                    $(this).find("label").text($(this).find("label").text()+" | "+result.marahel[(index_num)]);
                                    $(this).find("label").css({"width": "100%"});
                                }
                                $(this).find("label").attr("first_run", "false");
                            }
                            if( index >= (parseInt(result.marahel_count)*3 )){
                                $(this).fadeOut();
                            }else{
                                $(this).fadeIn();
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