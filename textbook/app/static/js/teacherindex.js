
var users_list=['ant', 'giraffe', 'penguin', 'sheep', 'hippo', 'lion', 'dolphin', 'eagle', 'frog', 'duck', 'bee', 'bat', 'elephant', 'leopard', 'panda', 'fish', 'fox', 'alligator', 'kangaroo', 'liger', 'squirrel', 'zebra', 'bear', 'deer', 'dog', 'tiger', 'monkey', 'rabbit', 'raccoon', 'AW', 'user1', 'user2']
var random_group_id
$(function(){
    console.log("teacherindex.js loaded");



    //loadtable();
    //loadGraph();

    showUserList();
    detectTableClick();
    dashboard();

    //https://stackoverflow.com/questions/21913283/how-to-catch-click-event-with-jquery-on-dynamically-created-button
    $('#tbody').on('click','.tchr-uname',function(e){

        console.clear();
        var username = $(this).attr('data-uname');

        //get image for this particular user
        var image_list = getImagePerUser(activity_id,username);
        //alert(image_list)
        tchr_showImageInGallery(image_list, "tchr-gallery")
        $('#teacher-gallery-table').hide();
        $('#tchr-gallery').show();

    });

    $('#backToTchrTable').click(function(e){
        e.preventDefault();
        $('#teacher-gallery-table').show();
        $('#tchr-gallery').hide();
    });

    $('.teacher-view').on('click', '.groupLink', function(e){
            e.preventDefault();
            random_group_id = $(this).attr('data-random-group-id');
            getRandomListData(random_group_id); //defined down below

      });

    //teacher card close button
    $('.teacher-card-close-button').on('click', function(e){

        $(this).closest('.card').removeClass('active');
    });


})

var dashboard = function(){

    //
    $(".dashboard_ka").click(function(){
        //get the activity id
        var dashboard_ka_id = $(this).data("dashboard-ka-id");
        //console.log(dashboard_ka_id);

        //clear any tables if present
        $("#dashboard-table").empty();

        var ka_table_info;
        $.ajax({
            type:'GET',
            url:'http://'+ host_url +'/getKAPerKAID/'+dashboard_ka_id,
            async: false, //wait for ajax call to finish
            success: function(e){
                ka_table_info = e.success;
                console.log(ka_table_info);
            }
        })
        //update the div with table
        var table = $('<table></table>').addClass('dashboard-table');
        table.append("<tr><td style='width:100px;'>User Name</td><td style='width:50px;'>Total Count</td><td>Student Response</td></tr>");
        $.each(ka_table_info, function(i, word) {
            console.log(word['response'])

            var markup = "<tr><td>" + word['posted_by'] + "</td><td style='width:50px;'>" + word['count'] + "</td><td>" + word['response'] + "</td></tr>";
            table.append(markup);

          });

         $("#dashboard-table").append(table);
    })

    $(".dashboard_gallery").click(function(){
        //get the activity id
        var dashboard_gid = $(this).data("dashboard-gid");

         //clear any tables if present
         $("#dashboard-table").empty();

         var gallery_table_info;
        $.ajax({
            type:'GET',
            url:'http://'+ host_url +'/getGalleryPerID/'+dashboard_gid,
            async: false, //wait for ajax call to finish
            success: function(e){
                gallery_table_info = e.success;
                console.log(gallery_table_info);
            }
        })

        //update the div with table
        var table = $('<table></table>').addClass('dashboard-table');
        table.append("<tr><td style='width:100px;'>User Name</td><td style='width:50px;'>Total Count</td><td>Student Response</td></tr>");
        $.each(gallery_table_info, function(i, word) {
            console.log(word['response'])

            var markup = "<tr><td>" + word['posted_by'] + "</td><td style='width:50px;'>" + word['count'] + "</td><td>" + word['comments'] + "</td></tr>";
            table.append(markup);

          });

         $("#dashboard-table").append(table);


    })



}

var showUserList = function(){

    //TODO: hide all other div except user list div
     $('#teacher-user-list').show();
     $('#single-user-view').hide();

    //generate button for all the users
    for(var i of users_list.sort()) {
        //can use break;
        //console.log(i); //note i returns value
//        var li = $("<li/>").appendTo('#teacher-user-list');
//        li.append('<a href="#" class="userprofile" data-username='+i+'> ' + i + '</a>'); //click detect handled in teacherindex.js

          var atag = $('ka-projection-number-display').appendTo('#teacher-user-list');
    }

    //reverse order
//    var list = $('#teacher-user-list');
//    var listItems = list.children('a');
//    list.empty();
//    list.append(listItems.get().reverse());

    $('#teacher-user-list').off().on('click', '.userprofile', function(e){
        //alert($(this).attr('data-username'));
        $('#teacher-user-list').hide();
        $('#single-user-view').show();

    });


}

var getRandomListData = function(groupid){
    $.ajax({
            type:'GET',
            url:'http://'+ host_url +'/getRandomListData/'+activity_id+'/'+groupid,
            async: false, //wait for ajax call to finish
            success: function(e){
                returnValue = e.success;
                $('.teacher-view').hide();
                middleGroupDiscussion = 'yes';
                showImageInGallery(returnValue); //defined in gallery.js

            }
        })

}

//called from digTextbook.js
var initStage = function(){

     //only show the user list -- hide rest of the divs
//     $('#teacher-user-list').show();
//     $('#single-user-view').hide();

        //lastOpenedTool variable is set in digTextbook.js when card tool is selected
        if(lastOpenedTool === 'khan_academy'){
            //alert('last opened tool was khan academy');
            //hide other div except khan academy
            $(".verticalDivider").show();
            $(".verticalDivider").siblings().hide();
            //close button display
            $(".teacher-card-close-button").show();

            //TODO: ajaxk call and get the values and replace the following texts

             var ka_post_length_odd_id = '';
             var ka_post_length_even_id = '';
             var odd_answer_count = '';
             var odd_question_count = '';
             var even_answer_count = '';
             var even_question_count = '';

             $.ajax({
                type:'GET',
                url:'http://'+ host_url +'/dashboardKAInfo/'+activity_id, //fetches number of groups, their user list and total number of comments
                async: false, //wait for ajax call to finish, else logged_in is null in the following if condition
                success: function(e){
                    ka_post_length_odd_id = e.ka_post_length_odd_id;
                    ka_post_length_even_id = e.ka_post_length_even_id;
                    odd_answer_count = e.odd_answer_count;
                    odd_question_count = e.odd_question_count;
                    even_answer_count = e.even_answer_count;
                    even_question_count = e.even_question_count;
                }
            });


            //display items
            $('.ka-projection-number-display-1').text(ka_post_length_odd_id);
            $('.ka-projection-number-display-2').text(ka_post_length_even_id);
            $('#post1-question-count').text(odd_question_count + ' question(s)');
            $('#post1-answer-count').text(odd_answer_count + ' answer(s)');
            $('#post2-question-count').text(even_question_count + ' question(s)');
            $('#post2-answer-count').text(even_answer_count + ' answer(s)');

        }if(lastOpenedTool === 'gallery'){
            //alert('last opened tool was gallery');
            //hide other div except gallery
            $(".gallery_middle").show()
            $(".gallery_middle").siblings().hide();
            $(".teacher-view").css("display", "block");
             //close button display
            $(".teacher-card-close-button").show();

//            var  list;
//             $.ajax({
//                type:'GET',
//                url:'http://'+ host_url +'/dashboardGalleryInfo', //fetches number of groups, their user list and total number of comments
//                async: false, //wait for ajax call to finish, else logged_in is null in the following if condition
//                success: function(e){
//                    list = e.list
//                    console.log(e.list);
//                }
//            });
//            //update a table with information from the list
//            $(".gallery_middle").empty();
//            var table = $('<table></table>')//.addClass('dashboard-table');
//            table.append("<tr><td style='width:100px;'>group id</td><td style='width:50px;'>total posts</td><td>response</td></tr>");
//            $.each(list, function(i, word) {
//                //console.log(word['response'])
//
//                var markup = "<tr><td>" + word['group_id'] + "</td><td style='width:50px;'>" + word['user_list'] + "</td><td>" + word['total_comment'] + "</td></tr>";
//                table.append(markup);
//
//              });
//
//            $(".gallery_middle").append(table);


        }



}
//called from digTextbook.js
var loadtable = function (activity_id){


}

var getGalleryInfo = function(activity_id){

    var returnValue = null;
    $.ajax({
            type:'GET',
            url:'http://'+ host_url +'/getGalleryTableTD/'+activity_id,
            async: false, //wait for ajax call to finish
            success: function(e){
                returnValue = e.success;

            }
        })

    return returnValue;

}

var getImagePerUser = function(activity_id, username){

    var returnValue = null;
    $.ajax({
            type:'GET',
            url:'http://'+ host_url +'/getImagePerUser/'+activity_id+'/'+username,
            async: false, //wait for ajax call to finish,
            success: function(data){
                returnValue = data.success;
            }
        })

    return returnValue;

}

var detectTableClick = function(){

        //detect when username in the table is clicked
        //https://stackoverflow.com/questions/1359018/in-jquery-how-to-attach-events-to-dynamic-html-elements
        $('body').on('click', 'a.cc', function() {
            // get the username who link was clicked
            var username = $(this).text();

        });
}



var tchr_showImageInGallery = function(data, gallery_type){

    $("#"+gallery_type).empty();

    var obj = jQuery.parseJSON(data);
     console.log(obj)

     $.each(obj, function(key,value) {

           console.log(value.fields) //gives all the value
           // console.log(value.fields['image']); //image field in the model
           //console.log(groupArray[value.fields['group_id']-1]); //group id of the user who uploaded it

           // console.log(logged_in, value.fields['posted_by'][0])
           // console.log('primary id::',value.pk)
           // console.log('total number of images: ', obj.length)

           var groupID = groupArray[value.fields['group_id']-1];

           var li = $("<li/>").appendTo("#tchr-gallery"); //<ul id=gallery>


           if(logged_in == value.fields['posted_by'][0]){

                //adding image delete span on the image
               var span = $('<span/>')
                    .addClass('object_delete')
                    .appendTo(li);

               var img = $('<img/>', {
               src : 'http://'+ host_url +'/media/'+value.fields['image'] })
               .css({opacity:1.0})
               .appendTo(li);

               var span_badge = $('<span/>')
                        .addClass('badge')
                        .text(groupID)
                        .appendTo(li);

              //add delete button functionality
               var closeBtn = $('<span class="object_delete"></span>');
               closeBtn.click(function(e){
                    card_extension_close();
                    e.preventDefault();
                    //get ID of the deleted note
                    var deletedImageID = value.pk;
                    console.log('deleted image id :: ', deletedImageID);
                    $(this).parent().remove(); //remove item from html

                    enterLogIntoDatabase('delete image', 'image delete from gallery' , 'image-delete-'+deletedImageID, 111)


                  //delete note from database
                    $.ajax({
                        type:'POST',
                        url:'/gallery/del/'+deletedImageID,
                        async: false, //wait for ajax call to finish,
                        success: function(e){
                            console.log(e)
                            //TODO: add user log

                        }
                    })


                    return false;
                });

                li.append(closeBtn);

            }else{

               //just add others image to the gallery
               var img = $('<img/>', {
               src : 'http://'+ host_url +'/media/'+value.fields['image'] }).appendTo(li);

                var span_badge = $('<span/>')
                        .addClass('badge')
                        .text(groupID)
                        .appendTo(li);

            }

           // Add clickhandler to open the single image view
           img.on('click', function(event){

               enterLogIntoDatabase('gallery image view', 'gallery individual image view' , 'image-select-id-'+value.pk , 111)

               //console.log($(this).parent().siblings().length); //+1 gives me the total number of images in the gallery
               totalPhoto = $(this).parent().siblings().length+1;

               //use the following value to navigate through the gallery
               //console.log($(this).parent().index()) //gives the index of li within the ul id = gallery
               $('.section input[name="image-index"]').attr('value', $(this).parent().index())

               openImageView($('#gallery-view'), $(this));


           });

        });

        //reverse the image order
        var list = $('#gallery');
        var listItems = list.children('li');
        list.append(listItems.get().reverse());

}




//var loadGraph = function(){
//
////    var line1 = [["10.01.2011",3.9990],["11.01.2011",3.9910],["12.01.2011",4.0140],["13.01.2011",3.9940],["14.01.2011",3.9050],["17.01.2011",3.9340],["18.01.2011",3.9520],["19.01.2011",3.8980],["20.01.2011",3.8690],["21.01.2011",3.8830],["24.01.2011",3.8550],["25.01.2011",3.8480],["26.01.2011",3.8190],["27.01.2011",3.8440],["28.01.2011",3.8260],["31.01.2011",3.8060],["01.02.2011",3.7970],["02.02.2011",3.8060],["03.02.2011",3.8110],["04.02.2011",3.8640],["07.02.2011",3.8750],["08.02.2011",3.8640],["09.02.2011",3.8480],["11.02.2011",3.8570],["14.02.2011",3.8880],["15.02.2011",3.88],["16.02.2011",3.8520],["17.02.2011",3.8590],["18.02.2011",3.8690],["22.02.2011",3.8440],["23.02.2011",3.8080],["24.02.2011",3.7410],["25.02.2011",3.7460],["28.02.2011",3.7550],["01.03.2011",3.7520],["02.03.2011",3.76],["03.03.2011",3.7420],["04.03.2011",3.7430],["07.03.2011",3.7330],["08.03.2011",3.7260],["09.03.2011",3.76],["10.03.2011",3.7910],["11.03.2011",3.79]];
////    var plot1 = $.jqplot('teacher-student-plot', [line1], {
////        title: 'User Participation Bar Chart',
////        axes: { xaxis: { renderer: $.jqplot.DateAxisRenderer } },
////        series: [{ lineWidth: 4, markerOptions: { style: 'square' } }]
////    });
//
//    var line1 = [['ant', 4],['fox', 6],['penguin', 2],['bat', 5],['panda', 6]];
//
//    $('#teacher-student-plot').jqplot([line1], {
//        title:'User Participation',
//        seriesDefaults:{
//            renderer:$.jqplot.BarRenderer,
//            rendererOptions: {
//                // Set the varyBarColor option to true to use different colors for each bar.
//                // The default series colors are used.
//                varyBarColor: true
//            }
//        },
//        axes:{
//            xaxis:{
//                renderer: $.jqplot.CategoryAxisRenderer
//            }
//        }
//    });
//
//
//}




