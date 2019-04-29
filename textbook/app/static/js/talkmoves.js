$(function(){

    copy_tm_text_button();


})

//badge banner copy implementaion
var copy_tm_text_button = function(value){

     $(document).on('click','.tm-row-copy-button.bannercopy',function(value){
     //$('#tm-row-copy-button').click(function(value){

        //https://jqueryhouse.com/copy-data-to-clipboard-using-jquery/
        var copied_text = $(this).parent().siblings().text();
        console.log("talkmoves.js", copied_text)
        if(!copied_text.trim()) {


        }else{
            console.log(copied_text);
            //alert(copied_text)
            var value = '<input value="'+ copied_text +'" id="selVal" />';
            $(value).insertAfter($(this));
            //$(value).insertAfter($('#ka-row-copy-button'));
            $("#selVal").select(); //select works for input //https://stackoverflow.com/questions/50941892/copy-to-clipboard-value-of-selected-option
            document.execCommand("copy");
            $('div.talkmoves-copy').find("#selVal").remove();

            //set to input field in chat
            //$('write-message#msg-text').val(copied_text)

            //alert("Copied the text: " + copied_text);

            //set to the message input box

        }

    })
}

