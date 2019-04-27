 var logged_in=''
 var host_url = window.location.host

 $( function() {

    getAnswers();

  } ); //end of page load function

var isAnswerNull = 0;

var getAnswers = function(){

    //handling persistence - start
    if(localStorage.getItem("answer_x")){

        $("textarea[name='nested-circle-x']").val(localStorage.getItem("answer_x"))

    }
    if(localStorage.getItem("answer_y")){

        $("textarea[name='nested-circle-y']").val(localStorage.getItem("answer_y"))

    }
    if(localStorage.getItem("answer_z")){

        $("textarea[name='nested-circle-z']").val(localStorage.getItem("answer_z"))

    }

     //handling persistence - end

    //nested circle input
    $("#nested-circle-submit").off().click(function(e){

        //multiple inputs instead of 1, store them in the array
        var answerArray = [];

        //get the answer from the textbox
        var answer_x = $("textarea[name='nested-circle-x']").val();
        var answer_y = $("textarea[name='nested-circle-y']").val();
        var answer_z = $("textarea[name='nested-circle-z']").val();


        //send to user lof db

        //send to database if the answer is not null
        if(!answer_x.trim() || !answer_y.trim() || !answer_z.trim()){

             showErrorMsg();

        }else{

                 //send to db and disable the submit button
                localStorage.setItem("answer_x", answer_x);
                localStorage.setItem("answer_y", answer_y);
                localStorage.setItem("answer_z", answer_z);


                //add all the data together
                answerArray.push(answer_x);
                answerArray.push(answer_y);
                answerArray.push(answer_z);

                console.log('answerArray', answerArray);

                 //array of answers, convert to json
                answerJson = JSON.stringify(answerArray);

                sendUserInputToDB(7, answerJson);

        }


    })





//    //page 7 input1
//    $("#page7-input1").off().click(function(e){
//
//        //multiple inputs instead of 1, store them in the array
//        var answerArray = [];
//
//        //variable used to see if any of the input is empty or not
//        var isAnswerNull = 0;
//
//        //get the answer from the textbox
//        $.each([1,2,3], function(index, value){
//
//            var answer = $("textarea[name='page7-input"+value+"']").val();
//
//            //handle empty input
//            if(!answer.trim()){
//
//                isAnswerNull = 1;
//
//            }else{
//                //add question so its easier to understand which answer refers to which question
//                var temp = {
//                    question: 'page7-input'+value,
//                    answer: answer.trim()
//                }
//
//                answerArray.push(temp);
//            }
//
//        });
//
//        //array of answers, convert to json
//        answerJson = JSON.stringify(answerArray);
//
//        //send to user lof db
//
//        //send to database if the answer is not null
//        if(isAnswerNull == 1){
//
//            showErrorMsg();
//
//            isAnswerNull = 0;
//
//        }else{
//
//            //send to db and disable the submit button
//            sendUserInputToDB(7, answerJson);
//            localStorage.setItem("page7input1", answerJson);
//            //$('#page7-input1').attr('disabled',true);
//
//        }
//
//    })


}

var sendUserInputToDB = function(page, value){


        $.post({


               async: false,
               url:'/submitAnswer',
               data: {
                    'page': page,
                    'answer': value
                    },
               success: function(response){

                    $("#myModal").css({ display: "block" });
                    $("#myModal h2").text("Your response was recorded");

                    $(".modal-close").click(function(e){
                         $("#myModal").css({ display: "none" });
                    });
            }

            });


            //send to user log as well
            enterLogIntoDatabase('submit pressed', 'answer question' , value, current_pagenumber)
}

var showErrorMsg = function(){

     modal = $("#myModal")

     $("#myModal").css({ display: "block" });
     $("#myModal h2").text("You’re missing one or more answers.");

     $(".modal-close").click(function(e){
         $("#myModal").css({ display: "none" });
     });

}