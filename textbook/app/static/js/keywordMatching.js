var keywords_obj = new Object();
    keywords_obj.social = "thanks,thank you,thankyou,love it,good job,great job,great";
    keywords_obj.explanation="because,cause,would be,but,since,for example,an example";
    keywords_obj.feedback = "correct,incorrect,correct answer,incorrect answer,right answer,didnt understand,did not understand,i understand";
    keywords_obj.suggestion = "i think,should,could be,try";
    keywords_obj.ques= "how,what,where,why,can you,did,do,does";
    keywords_obj.relevance = "sphere,cone,cylinder,area,volume,hemisphere,radius,diameter,circumference,pi,surface area";
    keywords_obj.reflection="i agree,i disagree,confused";
    keywords_obj.cocon="based on your idea,compare your answer to my answer,you did,like your,you did,you have done";

var badge_dict = {'suggestion': 'Suggestion', 'social' : 'Good Citizen', 'relevance' : 'Relevant Post', 'reflection' : 'Good Communication',
'ques' : 'Question', 'feedback' : 'Feedback', 'explanation' : 'Good Explanation', 'cocon': 'Co-Construction'};

var keywords_json = JSON.stringify(keywords_obj);

 $('.prompt-close-card').on('touch click', function(){

        $(this).closest('.prompt-card').removeClass('active');

    });


function showPrompt(message, platform){

    var msg = message.split(" ");
    var lengthOfMsg = msg.length;
    //console.log('message length :: ', lengthOfMsg);
    //alert(lengthOfMsg.length)


    if(lengthOfMsg == 0) return false;


    if(platform === 'ka'){
        if(lengthOfMsg < 20) return false;//word based
    }else{
        if(lengthOfMsg < 7) return false;//word based
    }

    message = message.toLowerCase();

    var prompt_text = ''

    //https://www.tjvantoll.com/2013/03/14/better-ways-of-comparing-a-javascript-string-to-multiple-values/
    //loop through key words
    $.each(keywords_obj, function(index, keywords) {
        //console.log(keywords.split(","))
        //console.log(message)

        var regexExactMatch = new RegExp('\\b' + keywords.split(",").join("|")+ '\\b');

        if(regexExactMatch.test(message)){

            //if question check if the question word is at the beginning of the sentence
            if(index === 'ques' && regexExactMatch.exec(message).index != 0) return false; //the question keyword is not the beginning so no badge

            //if matches with a badge already received before, return
            //https://stackoverflow.com/questions/18867599/jquery-inarray-how-to-use-it-right
            //if(jQuery.inArray(index, badges) > -1) return false;

            if(platform === 'ka'){
                $('.prompt-card.prompt-ka').addClass('active');
                $('#prompt-badge-img-ka').attr('src','/static/pics/'+index+'.png');
                $('p#prompt-p-ka').text("You earned a " + badge_dict[index] + " badge!");
            }else if(platform === 'gallery'){
                $('.prompt-card.prompt').addClass('active');
                $('#prompt-badge-img').attr('src','/static/pics/'+index+'.png');
                $('p#prompt-p').text("You earned a " + badge_dict[index] + " badge!");
            }else{
                $('.prompt-card.prompt-gm').addClass('active');
                $('#prompt-badge-img-gm').attr('src','/static/pics/'+index+'.png');
                $('p#prompt-p-gm').text("You earned a " + badge_dict[index] + " badge!");
            }

             //insert the badge in the database
             insertBadgeIngoinDB(message, index);
             displayAllBadges();
             //getBadgesFromDB();

             enterLogIntoDatabase('display prompt', 'badge:'+index , message, current_pagenumber)
             return false; //one badge at a time.


        }else{

        }

    });

}

var insertBadgeIngoinDB = function(message, badgeType){

    $.ajax({
            type:'POST',
            url:'http://'+ host_url +'/insertBadges/',
            async: false,
            data:{
                'message': message,
                'badgeType': badgeType

            },
            success: function(e){

            }
        })
}
