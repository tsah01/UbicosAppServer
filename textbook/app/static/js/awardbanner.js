var host_url = window.location.host
var badges = [];
var badge_count = [];
var dict = {'suggestion': false, 'social' : false, 'relevance' : false, 'reflection' : false, 'ques' : false, 'feedback' : false, 'explanation' : false, 'cocon' : false};

$(function(){

    displayAllBadges();


})

//$( document ).ready(function() {
//    setInterval(function(){
//    clearBadges();
//    displayAllBadges();
//    console.log("check check");
//    }, 5000);
//});


var getBadgesFromDB = function(){

    $.ajax({
        type:'GET',
        url:'http://'+ host_url +'/getBadges/',
        async: false,
        success: function(e){
            //returns an array of badges
            //console.log(e.badgeList)
            badges = e.badgeList;
        }
    })
}

function displayAllBadges(){
    //get badges from database
    clearBadges();
    getBadgesFromDB();
    //badges = ["social", "ques"];

    var src = $("#award-holder");

    for(var i = 0; i < badges.length; i++){
        dict[badges[i]] = true;
    }

    for(var key in dict){
        var divBnrHeader = $('<div style="margin-left:150px;"></div>');
        $(src).append(divBnrHeader);

        var divBnr = $('<div style="float:left"></div>');
        $(divBnrHeader).append(divBnr)


        var spandiv = $('<span class="imgtooltip"></span>');
        $(divBnr).append(spandiv)

        var img = document.createElement("img");

        if(dict[key])
            var img = $('<img/>', { id: key, src : 'http://'+ host_url + "/static/pics/" + key + ".png" }).css({"width":"30px", "margin-right": "5px", "margin-left": "5px"}).appendTo(divBnr);
            //img.appendTo(imgDivBnr);
        else
            var img = $('<img/>', { id: key,  src : 'http://'+ host_url + "/static/pics/" + "blank" + ".png" }).css({"width":"30px", "margin-right": "5px", "margin-left": "5px"}).appendTo(divBnr);
            //img.appendTo(imgDivBnr);
    }

    hoverBadge();
   // src.append("</center>");


  }

  function clearBadges(){

    for(var key in dict){
    //console.log("remove badge" + key);
    $('img#' + key).remove();
    }

  }

var badge_dict_description = {'suggestion': 'You get this badge when you provide suggestion',
'social' : 'You get this badge when you are social',
'relevance' : 'You get this badge when you post something related to the topic',
'reflection' : 'You get this badge when you explain your understanding',
'ques' : 'You get this badge when you ask a question',
'feedback' : 'You get this badge when you provide a feedback',
'explanation' : 'You get this badge when you provide explanation',
'cocon': 'You get this badge posting comment based on others comment'};

var badge_dict_example = {'suggestion': 'Next time try multiplication..',
'social' : 'Good job on the board we got the same answers on our board.',
'relevance' : 'The shape of the circle...',
'reflection' : 'I agree/disagree to your answer because....',
'ques' : 'What do you mean by that?',
'feedback' : 'The solution posted here are great..',
'explanation' : 'I think that this point is important, because…',
'cocon': 'If I compare your answer to my answer, I think....'};

var badge_dict_prompt_copy = {'suggestion': 'Next time try ...',
'social' : 'Thank you...',
'relevance' : 'The shape of the circle...',
'reflection' : 'I agree/disagree to your answer because....',
'ques' : 'Why did you...instead of...?',
'feedback' : 'The solution posted here are great..',
'explanation' : 'I think...because...',
'cocon': 'You did... but another way to do it is...'};

  function hoverBadge(){

   for(var key in dict){

        //$('#badge-description').children('img').remove();
        //$('#badge-description').show();

        //$("img#"+key).on("mouseover", function () {
        $("img#"+key).on("mouseenter", function () {

               $('#badge-description').show();
               $('#badge-description').empty();
                var display = $(this).attr('id');
                var badge_descript = $('#badge-description');

                $('#badge-description').append("<span onclick=this.parentElement.style.display='none' class='topright'>&times</span>")

                var img = $('<img/>', { id: display, src : 'http://'+ host_url + "/static/pics/" + display + ".png" }).css({"width":"50px", "margin-right": "5px", "margin-left": "5px"}).appendTo(badge_descript);

                $('#badge-description').append("<p id = 'badge_name'>" + badge_dict[display] + "</p>");

                $('#badge-description').append("<p id = 'badge_descrip'>"+badge_dict_description[display]+".</p>");

                $('#badge-description').append("<p id = 'badge_example' style='font-style:italic;'>"+badge_dict_example[display]+".</p>");

                var example_string =  "<div id='talkmoves-copy'><p id = 'badge_example' style='visibility: hidden;float: left;'>"+badge_dict_prompt_copy[display]+".</p>"+
               "<div class='tm-row'><input id='tm-row-copy-button' type='button' name='1' value='Copy' class='bannercopy'>"+
                "</div>"+
                "</div>"

                 $('#badge-description').append(example_string);
                 $('#badge-description').css('opacity','.9');




        }).on("mouseout", function(){
            //$('#badge-description').css('opacity','0');
            //clearTimeout(setTimeoutConst );

        });
    }

  }



