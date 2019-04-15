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

var badge_dict_description = {'suggestion': 'Suggestion Description', 'social' : 'Good Citizen Description', 'relevance' : 'Relevant Post Description',
'reflection' : 'Good Communication Description', 'ques' : 'Question Description', 'feedback' : 'Feedback Description',
'explanation' : 'Good Explanation description', 'cocon': 'Co-Construction description'};

var badge_dict_example = {'suggestion': 'Suggestion Example', 'social' : 'Good Citizen Example', 'relevance' : 'Relevant Post Example',
'reflection' : 'Good Communication Example', 'ques' : 'Question Example', 'feedback' : 'Feedback Example',
'explanation' : 'Good Explanation Example', 'cocon': 'Co-Construction Example'};

  function hoverBadge(){

   for(var key in dict){

        //$("img#"+key).on("mouseover", function () {
        $("img#"+key).on("mouseenter", function () {
             //stuff to do on mouseover
             //alert('here') //works
             //$('#badge-description').children('img').remove();
             $('#badge-description').show();
              $('#badge-description').empty();
             var display = $(this).attr('id');
             var badge_descript = $('#badge-description');

            $('#badge-description').append("<span onclick=this.parentElement.style.display='none' class='topright'>&times</span>")

             var img = $('<img/>', { id: display, src : 'http://'+ host_url + "/static/pics/" + display + ".png" }).css({"width":"50px", "margin-right": "5px", "margin-left": "5px"}).appendTo(badge_descript);

             $('#badge-description').append("<p id = 'badge_name'>" + badge_dict[display] + "</p>");

             $('#badge-description').append("<p id = 'badge_descrip'>"+badge_dict_description[display]+".</p>");

             $('#badge-description').append("<p id = 'badge_example'>"+badge_dict_example[display]+".</p>");

             $('#badge-description').css('opacity','1');
             console.log(key);


        }).on("mouseout", function(){
            //$('#badge-description').css('opacity','0');

        });
    }

  }



