
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .models import imageModel, imageComment, Message, brainstormNote,userLogTable, tableChartData, \
    userQuesAnswerTable, groupInfo, userLogTable, khanAcademyAnswer, random_group_users, badgeModel, \
    ActivityIndex, topics, modelbook, colorcode
from django.contrib.auth import authenticate
from django.http.response import JsonResponse
from django.contrib.auth import login as auth_login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.core import serializers
from .parser import parser
from .randomGroupGenerator import randomGroupGenerator
import json, random
from datetime import datetime, timedelta
from collections import Counter



# activity feed code -- start
from pusher import Pusher
from django.views.decorators.csrf import csrf_exempt

# instantiate the pusher class - this is used for activity feed message
pusher = Pusher(app_id=u'525110', key=u'ea517de8755ddb1edd03', secret=u'be2bf8ae15037bde9d94', cluster=u'us2')

# instantiate the pusher class - this is used for inidividual image message
pusher1 = Pusher(app_id=u'525110', key=u'f6bea936b66e4ad47f97', secret=u'ed3e9509fce91430fcac', cluster=u'us2')

# instantiate the pusher class - this is used for brainstorm note
pusher2 = Pusher(app_id=u'525110', key=u'5da367936aa67ecdf673', secret=u'e43f21c19211c9738d6b', cluster=u'us2')

@csrf_exempt
def broadcast(request):


    pusher.trigger(u'a_channel', u'an_event', {u'name': request.POST['username'], u'message': request.POST['message'] })

    #insert into database
    msg = Message(content=request.POST['message'], posted_by=request.user);
    msg.save();

    # print(image_data)

    return JsonResponse({'success': '', 'errorMsg': True})

# activity feed code -- end


@csrf_exempt
def broadcastImageComment(request):

    print('image broad cast', request.POST['discussion-type'])
    pusher1.trigger(u'b_channel', u'bn_event', {u'name': request.POST['username'], u'message': request.POST['message'], u'imageid': request.POST['imagePk'] })

    #get the image id
    img = imageModel.objects.get(id=request.POST['imagePk'])
    print('image primary id type',type(img))
    #error: id is not instance of the model
    #solution: https://www.slideshare.net/BaabtraMentoringPartner/how-to-fix-must-be-an-instance-when-a-foreign-key-is-referred-django-python-mysql
    comment = imageComment(content=request.POST['message'], posted_by = request.user, imageId = img, isGroupDiscussion=request.POST['discussion-type'])
    comment.save()

    return JsonResponse({'success': '', 'errorMsg': True})

@csrf_exempt
def broadcastBrainstormNote(request):

    #pusher2.trigger(u'c_channel', u'cn_event', {u'name': request.POST['username'], u'message': request.POST['message']})
    pusher2.trigger(u'c_channel', u'cn_event', {u'noteID': request.POST.get('brainstormID'), u'idea': request.POST.get('idea'),
                          u'color': request.POST.get('color'), u'posTop': request.POST.get('posTop'), u'posLeft': request.POST.get('posLeft'),
                          u'posted_by':request.POST['username'],
                          u'update': 'false'})

    note = brainstormNote(brainstormID=request.POST.get('brainstormID'), ideaText=request.POST.get('idea'),
                          color=request.POST.get('color'),
                          position_top=request.POST.get('posTop'), position_left=request.POST.get('posLeft'),
                          posted_by=request.user)
    note.save()

    note = brainstormNote.objects.last()
    print(note.id)
    return JsonResponse({'id': note.id, 'errorMsg': True})


#in the browser: http://127.0.0.1:8000/app/
def getUsername(request):
    if request.user.is_authenticated:
        print('username :: ', request.user.get_username())
        username = request.user.get_username();
        return JsonResponse({'name': username, 'errorMsg': True})


# My work starts from here(Tula)
@login_required
def index(request):
    if request.user.is_authenticated:
        #return render(request, 'app/index.html')
        #if teacher then open up teacher portal, else student portal
        if request.user.get_username() == 'teacher':
            usr = userLogTable.objects.all()
            activities = ActivityIndex.objects.all();
            return render(request, 'app/home.html', {'usrs': usr, 'activity': activities})
        else:
            return render(request, 'app/index.html')



# def activityList(request):
#     activities = ActivityIndex.objects.all();
#     return render(request, 'app/index.html',  {'activities': activities})



def teacher(request):
    return render(request, 'app/teacherindex.html')

def home(request):
    return render(request, 'app/home.html')

def ratio(request):
    return render(request, 'app/ratioProportion.html')

def volumeAndSurface(request):
    return render(request, 'app/VolumeAndSurface.html')

def linearFunction(request):
    return render(request, 'app/linearFunction.html')

def studentProfile(request):
    return render(request, 'app/studentProfile.html')



def login_form(request):
    return render(request, 'app/login.html',{})

def login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        # user is created using the createsuperuser command
        user = authenticate(username=username, password=password)
        print(user)

        if user:
            auth_login(request, user)
            #add to user log table
            userLog = userLogTable(username = request.user, action="user click login button", type="login", input=request.POST.get('username'), pagenumber=0000)
            userLog.save();

            # member = groupInfo(activityType='gallery', activityID=1, group=0, users=request.user)
            # member.save();

            return HttpResponseRedirect('/index/')
        else:
            #return invalid login message
            userLog = userLogTable(username=request.user, action="user click login button", type="invalid login",
                                   input=request.POST.get('username'), pagenumber=0000)
            userLog.save();



            return render(request, 'app/login.html', {})
    else:
        return render(request, 'app/login.html', {})


def uploadImage(request):
    #get image from html and save it in the database
    if request.method == "POST":
        # print (request.Files) #gives the name of the <input type='file' name...>

        #get the gallery ID
        gallery_id = request.POST.get('act-id')

        #get the group ID
        group_id = request.POST.get('group-id')

        # print(type(request.FILES['gallery_img'].name))
        # django.core.files.uploadedfile.InMemoryUploadedFile

        #get the logged in username
        username = ''
        if request.user.is_authenticated:
            print('username :: ', request.user.get_username())
            username = request.user.get_username();
        else:
            print('user not signed in') #add in log


        #insert values in the database
        #TODO: restrict insertion if user is not signed in
        img = imageModel(gallery_id=gallery_id, group_id = group_id , posted_by = request.user, image=request.FILES['gallery_img'])
        # TODO: check whether the insertion was successful or not, else wrong image will be shown using the last() query
        img.save()

        # using data NOT from database
        # data = {}
        # data['gallery_id'] = gallery_id
        # data['posted_by'] = username
        # # data['posted_at'] = "{}".format(images.posted_at)
        # data['url'] = 'images/'+request.FILES['gallery_img'].name
        # image_data = json.dumps(data)

        #get the latest inserted entry from the database for this particular group
        #https://stackoverflow.com/questions/2191010/get-last-record-in-a-queryset/21247350
        images = imageModel.objects.filter(group_id=group_id).last()

        print('image url :: ',images.image.url)

        print('user ::', images.posted_by.get_username())

        # using data from database
        data = {}
        data['image_id'] = images.pk
        data['gallery_id'] = images.gallery_id
        data['group_id'] = images.group_id
        data['posted_by'] = images.posted_by.get_username()
        data['posted_at'] = "{}".format(images.posted_at)
        data['url'] = images.image.url
        image_data = json.dumps(data)

        # print(image_data)
        #real time pic transfer
        # pusher1.trigger(u'b_channel', u'bn_event',
        #                 { u'new_image':image_data})

        return JsonResponse({'success': image_data, 'errorMsg': True})

def uploadKAImage(request):
    #get image from html and save it in the database
    if request.method == "POST":
        # print (request.Files) #gives the name of the <input type='file' name...>

        #get the KA ID
        ka_id = request.POST.get('ka-act-id');

        #get the logged in username
        username = ''
        if request.user.is_authenticated:
            print('username :: ', request.user.get_username())
            username = request.user.get_username();
        else:
            print('user not signed in') #add in log

        #insert values in the database
        ka_image_upload = khanAcademyAnswer(ka_id=ka_id, ka_image=request.FILES['ka_img_name'], posted_by=request.user);
        # TODO: check whether the insertion was successful or not, else wrong image will be shown using the last() query
        ka_image_upload.save();

        latest_upload = khanAcademyAnswer.objects.filter(ka_id=ka_id).last()
        #https://stackoverflow.com/questions/16640021/django-object-is-not-iterable-using-serializers-serialize
        ka_img = serializers.serialize('json', [latest_upload], use_natural_foreign_keys=True)
        #print(latest_upload.pk)

        return JsonResponse({'ka_imgID': latest_upload.pk, 'ka_img':ka_img})

def getImage(request, view_id, gallery_id,group_id):

    # for pilot/study
    if(int(view_id) == 1): #view_id = 1 means comment view
        #images = imageModel.objects.exclude(group_id=group_id)
        #images = images.filter(gallery_id=gallery_id)
        images = imageModel.objects.filter(gallery_id=gallery_id)
    else:
        images = imageModel.objects.filter(gallery_id=gallery_id)
        images = images.filter(group_id=group_id)

    # for workshop
    # images = imageModel.objects.filter(group_id=group_id)
    # images = images.filter(gallery_id=gallery_id)

    image_data = serializers.serialize('json', images, use_natural_foreign_keys=True)
    #print(image_data)
    #get and send random group information here

    random_group_list = getRandomGroupMemberList(request, gallery_id)
    random_group_list.remove('AW')  # remove simply removes the item, does not return anything. so print the list again

    return JsonResponse({'success': image_data, 'random_group_list':random_group_list})

def getImageID(request,img_filename):
    print('receiving parameter :: file name :: ' + img_filename);

    img = imageModel.objects.filter(image='images/'+img_filename)
    image_data = serializers.serialize('json', img, use_natural_foreign_keys=True)
    #print(image_data[0].fields)
    #print(img[0].pk)
    return JsonResponse({'imageData': image_data})

def getImagePerUser(request, act_id, username):
    print('receiving parameter :: activity id :: username ' + act_id + '  ' + username);

    image_list = imageModel.objects.filter(gallery_id=act_id).filter(posted_by=User.objects.get(username=username))
    image_data = serializers.serialize('json', image_list, use_natural_foreign_keys=True)

    print(image_data)

    return JsonResponse({'success': image_data})

def imageDelete(request, img_id):

    img = imageModel.objects.get(pk=img_id)
    # This will delete the image and all of its Entry objects.
    print(img)
    img.delete()

    return HttpResponse('deleted?')

def updateFeed(request, type):

    # # message of all times
    # msg = Message.objects.all()
    # msg_data = serializers.serialize('json', msg, use_natural_foreign_keys=True)
    # return JsonResponse({'success': msg_data, 'username': request.user.get_username(), 'errorMsg': True})


    if int(type) == 0:
        #message of all times
        msg = Message.objects.all()
        msg_data = serializers.serialize('json', msg, use_natural_foreign_keys=True)
        return JsonResponse({'success': msg_data, 'username': request.user.get_username(), 'errorMsg': True})
    elif int(type) == 1:
        #separate message today vs other days
        msg = Message.objects.filter(posted_at__gte = datetime.now() - timedelta(days=1)) #returns all the comment from today
        msg_data = serializers.serialize('json', msg, use_natural_foreign_keys=True)
        print('msg :: ', msg_data)
        return JsonResponse({'success': msg_data, 'username': request.user.get_username(), 'errorMsg': True})

    # #separate message today vs other days
    # msg = Message.objects.exclude(posted_at__contains = datetime.now().date()) #returns all the comment except from today
    # msg_data = serializers.serialize('json', msg, use_natural_foreign_keys=True)
    # print('msg :: ', msg_data)
    # return HttpResponse('')

def updateImageFeed(request, img_id):

    print('updateImageFeed (image_id) :: ' + img_id)
    img_msg = imageComment.objects.filter(isGroupDiscussion='no').filter(imageId_id=img_id)
    img_msg = serializers.serialize('json', img_msg, use_natural_foreign_keys=True, use_natural_primary_keys=True)

    return JsonResponse({'success': img_msg, 'username': request.user.get_username(),'errorMsg': True})

def brainstormSave(request):

    note = brainstormNote(brainstormID = request.POST.get('brainstormID'), ideaText = request.POST.get('idea'), color = request.POST.get('color'),
                              position_top = request.POST.get('posTop'), position_left = request.POST.get('posLeft'), posted_by = request.user)
    note.save()

    note = brainstormNote.objects.last()
    print(note.id)
    return JsonResponse({'id': note.id,'errorMsg': True})


def brainstormGet(request,brainstorm_id):

    notes = brainstormNote.objects.filter(brainstormID=brainstorm_id)
    notes = serializers.serialize('json', notes, use_natural_foreign_keys=True)

    return JsonResponse({'success': notes})


def brainstormUpdate(request, note_id):

    note = brainstormNote.objects.filter(id=note_id)

    pusher2.trigger(u'c_channel', u'cn_event',
                    {u'noteID': note_id, u'idea': note[0].ideaText,
                     u'color': note[0].color, u'posTop': request.POST.get('top'),
                     u'posLeft': request.POST.get('left'),
                     u'posted_by': request.POST.get('username'),
                     u'update': 'true'})

    brainstormNote.objects.filter(id=note_id).update(position_top=request.POST.get('top'),
                                                     position_left=request.POST.get('left'))
    return HttpResponse('')

def brainstormDelete(request,note_id):

    print('NOTEID', note_id);

    b = brainstormNote.objects.get(pk=note_id)
    # This will delete the Blog and all of its Entry objects.
    print(b)
    b.delete()

    return HttpResponse('no delete?')


def userlog(request):

    log = userLogTable(username=request.user, action=request.POST.get('action'), type=request.POST.get('type'),
                       input=request.POST.get('input'), pagenumber=request.POST.get('pagenumber'))
    log.save()

    return HttpResponse('')



def tableEntriesSave(request):

    entries = tableChartData(posted_by = request.user, table_id = request.POST.get('table_id'), plot_type = request.POST.get('plot_type'),
                             plot_data = request.POST.get('plot_data'))
    entries.save()

    return HttpResponse('')


def submitAnswer(request):

    print(request.POST.get('answer'));
    userQuesAnswer = userQuesAnswerTable(questionIDbyPage = request.POST.get('page'), answer = request.POST.get('answer'), posted_by = request.user)
    userQuesAnswer.save()

    return HttpResponse('')

def submitKAAnswer(request):
    #check if any query present for that KA

    #TODO: try update_or_create method
    if khanAcademyAnswer.objects.filter(ka_id=request.POST.get('activity_id')).filter(pk=request.POST.get('imgID')).filter(posted_by=request.user).exists():

        khanAcademyAnswer.objects.filter(ka_id=request.POST.get('activity_id')).filter(pk=request.POST.get('imgID')).filter(posted_by=request.user).\
            update(response_type=request.POST.get('response_type'),response=request.POST.get('answer'))

    #     khanAcademyAnswer.objects.filter(ka_id=request.POST.get('id')).filter(response_type=request.POST.get('response_type')).update(response=request.POST.get('answer'))
    # else:
    #     ka_answer = khanAcademyAnswer(ka_id=request.POST.get('id'), response_type=request.POST.get('response_type'), response=request.POST.get('answer'), posted_by = request.user)
    #     ka_answer.save()

    return HttpResponse('from server')



def checkKAAnswer(request, ka_id):

    try:
        #if multiple image with same ka activity id, pull the latest one
        ka_obj = khanAcademyAnswer.objects.filter(ka_id=ka_id).filter(posted_by=request.user).order_by('-pk')[:1];
        ka_obj = serializers.serialize('json', ka_obj, use_natural_foreign_keys=True)
        print(ka_obj)
    except imageModel.DoesNotExist:
        ka_obj = None

    return JsonResponse({'success': ka_obj})


def random_discussion_group_generator(request):

    #delete previoud grouping - if any
    random_group_users.objects.all().delete();

    #TODO: username and user face to face group number array
    self = None;
    all_group_list  = randomGroupGenerator.creategroup(self)
    for i in range(1,4):
        #iterate through the list of lists
        for list in  all_group_list:
            print(list)

            #get user for username=AW
            teacher_user = User.objects.get(username='AW')
            #iterate through the list and make entry

            for g in list:
                user =  User.objects.get(username=g)
                print(user)
                group_member = random_group_users(users=user, gallery_id = i, group=all_group_list.index(list)+1) #plus 1 so the group number starts from 1 instead of 0
                group_member.save();

                #add amanda in every group
            group_member = random_group_users(users=teacher_user, gallery_id = i, group=all_group_list.index(list)+1)
            group_member.save();


    # for i in range(1, 7): #6 galleries, so upto 7
    #     users_list = [str(user) for user in User.objects.all()];
    #     users_list = [n for n in users_list if n not in ['AW', 'user1', 'user2']]
    #     print(users_list)
    #     member_limit = 5;
    #
    #     users_list_copy = users_list
    #     group_list = []
    #     while len(users_list_copy) > 0:  # use all users
    #         if (len(users_list_copy) < member_limit):
    #             used_users = users_list_copy
    #             username_list_2 = [n for n in users_list_copy if n not in used_users]
    #             group_list.append(used_users)
    #             #print('groups:: ', used_users)
    #             break
    #         used_users = random.sample(users_list_copy, member_limit)
    #         group_list.append(used_users)
    #         #print('groups:: ', used_users)
    #         users_list_copy = [n for n in users_list_copy if n not in used_users]
    #         #print(users_list_copy)
    #
    #     #print(group_list)
    #
    #     #get user for username=AW
    #     teacher_user = User.objects.get(username='AW')
    #     #iterate through the list and make entry
    #     for group_index in range(len(group_list)):
    #         group = group_list[group_index]
    #         for g in group:
    #             user =  User.objects.get(username=g)
    #             print(user)
    #             group_member = random_group_users(users=user, gallery_id = i, group=group_index+1) #plus 1 so the group number starts from 1 instead of 0
    #             group_member.save();
    #
    #         #add amanda in every group
    #         group_member = random_group_users(users=teacher_user, gallery_id = i, group=group_index+1)
    #         group_member.save();

    #end of for loop
    return HttpResponse('')

    # # check if a user has joined a group or not; if not add him in a group if group has still empty place
    # # https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist
    # try:
    #     isUserPresent = random_group_users.objects.get(users_id=request.user)
    #     print('inside try', isUserPresent)
    #     return HttpResponse('unable to join the group, already joined a group')
    # except random_group_users.DoesNotExist:
    #     print('inside except')
    #     isUserPresent = None
    #     # count total number of members in the group
    #     member_count = random_group_users.objects.filter(group='A').count()
    #     print('total member count', member_count)
    #     if member_count < 6: #allows 6 members
    #         group_member = random_group_users(users = request.user, group='A')
    #         group_member.save();
    #         return HttpResponse('successfully joined the group')
    #     else:
    #         return HttpResponse('unable to join the group, group exceeded 6 members')

# called from gallery.js
def  getMediumGroupDiscussion(request):

    gallery_id = request.POST.get('gallery_id');

    #first filter based on gallery since each gallery has different random group
    random_users_based_on_gallery = random_group_users.objects.filter(gallery_id=gallery_id)

    #get in which middle group for current user
    middlegroup_id = random_users_based_on_gallery.get(users_id=request.user).group #get the query first and access the group from that query

    image_data_all = aux_method_get_img_random_list_group(middlegroup_id, gallery_id)

    return JsonResponse({'success': image_data_all})

def getRandomListData(request, gallery_id,group_id):

    image_data_all = aux_method_get_img_random_list_group(group_id, gallery_id)

    return JsonResponse({'success': image_data_all})

def aux_method_get_img_random_list_group(middlegroup_id, gallery_id):

    # first filter based on gallery since each gallery has different random group
    random_users_based_on_gallery = random_group_users.objects.filter(gallery_id=gallery_id)

    # find other users in this group
    middlegroup_users = random_users_based_on_gallery.filter(group=middlegroup_id)
    for o in middlegroup_users: print(o.users_id)

    # get their original group from groupinfo table
    image_data_all = []
    originalgroup_list = []
    for o in middlegroup_users:
        group_id = groupInfo.objects.filter(users_id=User.objects.get(pk=o.users_id)).order_by('group').values('group').distinct()[0]['group']

        originalgroup_list.append(group_id);

    # if same id twice -- image is displayed twice -- so get the distinct IDs of the image e.g., [7,7,1,4]
    originalgroup_list = list(set(originalgroup_list))
    print(originalgroup_list)

    for oid in originalgroup_list:
        #for each original group id get the image posted by that group - there should one image per group atleast
        images = imageModel.objects.filter(gallery_id=gallery_id)
        images = images.filter(group_id=oid)

        image_data = serializers.serialize('json', images, use_natural_foreign_keys=True)
        image_data_all.append(image_data)


    print(image_data_all)

    return image_data_all

# check random_group_users table for distinct group numbers, converts the query into list
# returns the list of groups
# called from digTextbook.js
def randomDiscussionList(request):
    #get total groups
    middlegroup_id = random_group_users.objects.values('group').distinct()

    #convert query into list
    middlegroup_id_list = [int(q["group"]) for q in middlegroup_id]
    print('randomDiscussionList method: ', middlegroup_id_list)

    return JsonResponse({'list': middlegroup_id_list})


# projection gallery dashboard
def dashboardGalleryInfo(request,act_id):
    gallery_id = act_id;

    # get total groups for this gallery
    info_query = random_group_users.objects.filter(gallery_id=gallery_id).values('group').distinct()

    # convert query into list
    group_list = [int(q["group"]) for q in info_query]

    list=[]
    for group_id in group_list:
        dict={};

        #store group id for this particular gallery
        dict['group_id'] = group_id

        info_query = random_group_users.objects.filter(gallery_id=gallery_id).filter(group=group_id)

        # store user list for this group for this gallery
        # get the user id from the users table and get their username

        temp = [User.objects.get(pk=e.users_id).get_username() for e in info_query]
        temp.remove('AW') #remove simply removes the item, does not return anything. so print the list again
        dict['user_list'] = temp
        #print(dict['user_list'])

        # get the total number of comments by the users for each group for this gallery
        image_data = aux_method_get_imgcomment_random_list_group_teacher(group_id, gallery_id)
        dict['total_comment'] = len(image_data)

        list.append(dict);

    #print([q["fields"] for q in info_query])
    return JsonResponse({'list': list})


def getRandomGroupMemberList(request, gallery_id):

    # get the group for the user for specific gallery
    random_group_id = random_group_users.objects.filter(gallery_id=gallery_id).filter(users_id=request.user).values('group')
    for o in random_group_id: random_group_id = o['group']

    #get the user list - this returns a query object
    random_list = random_group_users.objects.filter(gallery_id=gallery_id).filter(group=random_group_id)

    #convert the query list into a list
    random_group_list = [User.objects.get(pk=o.users_id).get_username() for o in random_list]

    return random_group_list;

def updateDiscussionImageFeed(request, gallery_id):

    print("updateDiscussionImageFeed");

    print("updateDiscussionImageFeed glry id", gallery_id)
    # first filter based on gallery since each gallery has different random group
    random_users_based_on_gallery = random_group_users.objects.filter(gallery_id=gallery_id)

    # get in which middle group for current user
    middlegroup_id = random_users_based_on_gallery.get(users_id=request.user).group  # get the query first and access the group from that query
    print("updateDiscussionImageFeed random group", middlegroup_id)

    image_data = aux_method_get_imgcomment_random_list_group_teacher(middlegroup_id, gallery_id)
    image_data = serializers.serialize('json', image_data, use_natural_foreign_keys=True)

    return JsonResponse({'success': image_data, 'username': request.user.get_username(), 'errorMsg': True})

def updateDiscussionImageFeedTeacherVersion(request, gallery_id, group_id):
    print('updateDiscussionImageFeedTeacherVersion', gallery_id)
    print('updateDiscussionImageFeedTeacherVersion',group_id)
    image_data = aux_method_get_imgcomment_random_list_group_teacher(group_id, gallery_id)
    image_data = serializers.serialize('json', image_data, use_natural_foreign_keys=True)
    return JsonResponse({'success': image_data, 'username': request.user.get_username(), 'errorMsg': True})

def aux_method_get_imgcomment_random_list_group_teacher(middlegroup_id, gallery_id):
    # find other users in this group
    # first filter based on gallery since each gallery has different random group
    random_users_based_on_gallery = random_group_users.objects.filter(gallery_id=gallery_id)

    middlegroup_users = random_users_based_on_gallery.filter(group=middlegroup_id)
    for o in middlegroup_users: print("updateDiscussionImageFeed random grp members", o.users_id)

    # get their original group from groupinfo table
    image_pk = []
    for o in middlegroup_users:
        originalgroup_id = \
        groupInfo.objects.filter(users_id=User.objects.get(pk=o.users_id)).order_by('group').values('group').distinct()[
            0]['group']

        print("updateDiscussionImageFeed original group id", originalgroup_id)
        # for each original group id get the image posted by that group - there should one image per group atleast
        images = imageModel.objects.filter(gallery_id=gallery_id).filter(group_id=originalgroup_id).values('pk')
        print("updateDiscussionImageFeed", images)

        for im in images:
            image_pk.append(im['pk']);
        # image_data = serializers.serialize('json', images, use_natural_foreign_keys=True)

    # image ids of the images that a group can see.
    # print('with duplicates :: ',image_pk)

    # if same id twice -- image is displayed twice -- so get the distinct IDs of the image
    image_pk = list(set(image_pk))
    # print('without duplicates :: ',image_pk)

    #get user object for middle group users
    userobject_list = []
    for o in middlegroup_users:
        userID = User.objects.get(pk=o.users_id)
        userobject_list.append(userID)

    # https://stackoverflow.com/questions/34830595/how-to-perform-a-queryset-in-django-with-a-loop-for-in
    image_data = imageComment.objects.filter(isGroupDiscussion='yes').filter(imageId_id__in=image_pk).filter(posted_by_id__in=userobject_list)
    print(image_data)

    return image_data

def getKAPerKAID(request,ka_id):


    plusone = int(ka_id) + 1
    #gives the raw query object
    ka_items = khanAcademyAnswer.objects.filter(ka_id__in=[ka_id, str(plusone)]).order_by('posted_by__username') #posted by is the foreign key, so it was sorting based on the
                                                                                            #id, posted_by__username sorts alphabetically.

    #user id who posted
    userid_list = [User.objects.get(pk=user['posted_by_id']).get_username() for user in khanAcademyAnswer.objects.values('posted_by_id').distinct()]
    #print(userid_list)
    #find users who did not post
    users_did_not_post = [x for x in getAllUserList() if x not in userid_list]
    #print(len(users_did_not_post))
    #print(users_did_not_post)


    #count number of student post
    counter = Counter()
    for o in ka_items:
        counter[o.posted_by.get_username()] += 1;

    ka_list = []
    #add users who did not post anything #not so happy with this approach #remove starts here
    for o in users_did_not_post:
        data = {}
        data['ka_image'] = '';
        data['posted_by'] = o;
        data['count'] = 0;
        data['response_type'] = '';
        data['response'] = '';
        #json_data = json.dumps(data);
        ka_list.append(data);
    # remove finishes here

    #iterate over the query
    for o in ka_items:
        data = {}
        data['ka_image'] = str(o.ka_image);
        data['posted_by'] = o.posted_by.get_username();
        data['count'] = counter[o.posted_by.get_username()];
        data['response_type'] = o.response_type;
        data['response'] = o.response;
        #json_data = json.dumps(data);
        ka_list.append(data);

    #sort list of dictionary items by their username
    #ka_list = sorted(ka_list, key=lambda k: k['posted_by'])

    #sort list by their counts
    ka_list = sorted(ka_list, key=lambda k: k['count'])

    # context = {
    #     'list': ka_list,
    #
    # }
    #return render(request, 'app/dashboard.html', context); #sent to html itself

    return JsonResponse({'success': ka_list});

def getGalleryPerID(request,gid):

    #gives the raw query object
    images = imageModel.objects.filter(gallery_id=gid)

    # user id who posted
    userid_list = []
    # image id list for this particular gallery
    image_list = []
    for im in images:
        comment_count_list = []
        comment_count_list = [0] * 31
        item = {}
        item['image_id'] = im.pk
        item['posted_by'] = im.posted_by.get_username()
        userid_list.append(item['posted_by'])
        image_comments = imageComment.objects.filter(imageId = im.pk)
        item['comments'] = [im.content for im in image_comments]
        item['count'] = len(item['comments'])
        image_list.append(item)

    #print(image_list)
    # find users who did not post
    users_did_not_post = [x for x in getAllUserList() if x not in userid_list]

    for user in users_did_not_post:
        item = {}
        item['image_id'] = 0;
        item['posted_by'] = user;
        item['comments'] = []
        item['count'] = 0
        image_list.append(item)

    # sort list by their counts
    image_list = sorted(image_list, key=lambda k: k['count'])

    return JsonResponse({'success': image_list});

def getDashboard(request):
    return render(request, 'app/dashboard.html');

def insertBadges(request):
    badge = badgeModel(badgeType = request.POST.get('badgeType'), message = request.POST.get('message'),
                       platform = request.POST.get('platform'), userid = request.user)
    badge.save()

    return HttpResponse('')

def getBadges(request):
    badges = badgeModel.objects.filter(userid=request.user).values('badgeType').distinct()

    badgeList = []
    for badge in badges:
        print(badge['badgeType'])
        badgeList.append(badge['badgeType'])

    #print(badgeList)

    badge_count = badgeModel.objects.values('badgeType').annotate(dcount=Count('badgeType'))
    print(badge_count)

    return JsonResponse({'badgeList': badgeList})

def pageParser(request):
    #CASE 4: static method - FAIL, not possible to call `cls.get` or `self.get`
    #ref: https://stackoverflow.com/questions/50806626/django-calling-one-class-method-from-another-in-class-based-view
    self = None
    print(parser.activityParser(self))
    return HttpResponse('')

def getUserList(request):
    users = User.objects.all()
    print(users)
    context = {'user_list': users}
    return render(request, 'app/studentList.html', context)


def getAllStudentInfo(request,std_id):
    return HttpResponse(std_id)


def dashboardKAInfo(request,ka_id):

    print('entering dashboardKAInfo ka_id:', ka_id);

    ka_id = int(ka_id)
    if ka_id%2 == 0:
        even_id = ka_id;
        odd_id = ka_id-1;
    else:
        odd_id = ka_id;
        even_id = ka_id+1;

    # post - 1
    odd_post_object = khanAcademyAnswer.objects.filter(ka_id = odd_id).exclude(response_type='')
    ka_post_length_odd_id = len(odd_post_object)
    print('hojoborolo',len(odd_post_object))

    #how many are question and how many are answer
    post_odd_count = odd_post_object.values('response_type').annotate(dcount=Count('response_type'))
    print(post_odd_count)  #output in the format --> {{response type:answer, dcount:2}, {response type:question, dcount:1})

    answer =  0
    question = 0

    for q in post_odd_count:
        print(q)
        if 'answer' in q.values():
            answer = q["dcount"]
        #else: answer = 0;

        if 'question' in q.values():
            question = q["dcount"]
        #else: question = 0;

    odd_answer_count = answer
    odd_question_count = question


    #post - 2
    post_even_object = khanAcademyAnswer.objects.filter(ka_id=even_id).exclude(response_type='')
    ka_post_length_even_id = len(post_even_object)

    # how many are question and how many are answer
    post_even_count = post_even_object.values('response_type').annotate(dcount=Count('response_type'))

    answer = 0
    question = 0

    for q in post_even_count:
        print(q)
        if 'answer' in q.values():
            answer = q["dcount"]
        #else: answer = 0;

        if 'question' in q.values():
            question = q["dcount"]
        #else: question = 0;

    even_answer_count = answer
    even_question_count = question



    return JsonResponse({'ka_post_length_odd_id': ka_post_length_odd_id, 'odd_answer_count':odd_answer_count, 'odd_question_count':odd_question_count,
                         'ka_post_length_even_id':ka_post_length_even_id, 'even_answer_count':even_answer_count, 'even_question_count':even_question_count})

def getGalleryTableTD(request, act_id):

    #get all the users
    users_list = [str(user) for user in User.objects.all()]
    print(users_list)
    #returns None if no object is returned from the query. handles exception/error.s
    try:
        images = imageModel.objects.filter(gallery_id=act_id)
    except imageModel.DoesNotExist:
        images = None

    image_list = []
    for im in images:
        comment_count_list = []
        comment_count_list = [0] * 31
        item = {}
        item['image_id'] = im.pk
        item['posted_by'] = im.posted_by.get_username()
        image_comments = imageComment.objects.filter(imageId = im.pk)
        item['comments'] = [im.content for im in image_comments]
        temp = [im.posted_by.get_username() for im in image_comments]
        temp = Counter(temp)
        for key, value in temp.items():
            index = [users_list.index(key)] #returns a list of one item
            comment_count_list[index[0]] = value;


        item['comment_count'] = comment_count_list
        image_list.append(item)

    return JsonResponse({'success': json.loads(json.dumps(image_list)), 'errorMsg': True})

# create superuser
# https://docs.djangoproject.com/en/2.1/topics/auth/default/
def registerUser(request):
    return render(request, 'app/register.html', {})

def createUser(request):

    if request.method == "POST":
        #get username/password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(username, '', password)
        user.save()

        #authenticate and redirect to index
        user = authenticate(username=username, password=password)
        print(user)

        if user:
            auth_login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            # return invalid login message
            return render(request, 'app/login.html', {})

    return HttpResponse('')

#temp solution for pilot-1 -- start
def groupAdd(request):

    users_list = [str(user) for user in User.objects.all()]
    print(len(users_list))

    usernames_array = ["giraffe", "raccoon", "ant", "tiger", "sheep", "deer", "panda", "liger", "fox", "hippo", "alligator",
                       "dog", "dolphin", "eagle", "zebra", "rabbit", "bear","monkey", "leopard", "frog", "squirrel", "elephant", "bee",
                       "duck", "kangaroo", "penguin", "fish","bat", "lion", "AW", "user1", "user2"];


    # for username in users_list:
    #     print(usernames_array.index(username))

    username_groupID = ['1', '1', '2', '2', '2', '3', '3', '3', '4', '4', '4', '5', '5', '5', '6', '6', '6','7', '7',
                        '7', '8', '8', '8', '9', '9', '9','10', '10', '10', '11', '11', '11']

    for i in range(len(usernames_array)):
        print (usernames_array[i], ' ----- ', username_groupID[usernames_array.index(usernames_array[i])]);


    # 4 gallery activities so range is from 1 to 5 (first study)
    # 6 gallery activities so range is from 1 to 7 (second study)

    for username in users_list:
        for i in range(1, 7):
            member = groupInfo(activityType='gallery', activityID=i, group=username_groupID[usernames_array.index(username)],
                               users=User.objects.get(username=username))
            member.save();

    return HttpResponse('')

def getGroupID(request, act_id):
    print('line 384 From server activity id', act_id)
    groupID = groupInfo.objects.all().filter(activityID = act_id)
    print('from server group id', groupID[0].group)
    groupID = groupID.filter(users_id = request.user)
    print(type(groupID))
    print('line 358',groupID[0].group)

    return HttpResponse(groupID[0].group)

# temp solution for pilot-1 -- end

def camera(request):
    return render(request, 'app/camera.html', {})


@csrf_exempt
def userLogFromExtenstion(request):
    #https://stackoverflow.com/questions/35474259/django-middleware-making-post-request-blank
    body = request.body.decode('utf-8')  # in python 3 json.loads only accepts unicode strings
    body = json.loads(body)

    print(body)
    username = body['username'].split(' ')[0].lower()
    action = body['action']
    type = body['type']
    data = body['input']
    pagenumber = body['pagenumber']

    print(username)
    user_pk_id = User.objects.get(username=username).pk
    print (user_pk_id)

    print('from extension?', username, action, type, data, pagenumber)
    log = body
    f = open("extensionLOGfile.txt", "a")
    f.write(str(log))
    f.write('\n')

    log = userLogTable(username=User.objects.get(pk=user_pk_id), action=body['action'], type=body['type'],
                       input=body['input'], pagenumber=body['pagenumber'])
    log.save()

    return HttpResponse('')

# hacks - start


def createBulkUser(request):

    # 29 user for the study + 3 user

    #group 1
    user = User.objects.create_user('panda', '', 'panda');
    user.save();
    user = User.objects.create_user('liger', '', 'liger');
    user.save();
    user = User.objects.create_user('sheep', '', 'sheep');
    user.save();

    # group 2
    user = User.objects.create_user('fox', '', 'fox');
    user.save();
    user = User.objects.create_user('leopard', '', 'leopard');
    user.save();
    user = User.objects.create_user('zebra', '', 'zebra');
    user.save();

    # group 3
    user = User.objects.create_user('bat', '', 'bat');
    user.save();
    user = User.objects.create_user('dog', '', 'dog');
    user.save();
    user = User.objects.create_user('squirrel', '', 'squirrel');
    user.save();

    #group 4
    user = User.objects.create_user('dolphin', '', 'dolphin');
    user.save();
    user = User.objects.create_user('elephant', '', 'elephant');
    user.save();
    user = User.objects.create_user('tiger', '', 'tiger');
    user.save();

    #group 5
    user = User.objects.create_user('fish', '', 'fish');
    user.save();
    user = User.objects.create_user('frog', '', 'frog');
    user.save();
    user = User.objects.create_user('monkey', '', 'monkey');
    user.save();

    #group 6
    user = User.objects.create_user('ant', '', 'ant');
    user.save();
    user = User.objects.create_user('kangaroo', '', 'kangaroo');
    user.save();
    user = User.objects.create_user('rabbit', '', 'rabbit');
    user.save();


    #group-7
    user = User.objects.create_user('bear', '', 'bear');
    user.save();
    user = User.objects.create_user('duck', '', 'duck');
    user.save();
    user = User.objects.create_user('hippo', '', 'hippo');
    user.save();


    #group 8
    user = User.objects.create_user('giraffe', '', 'giraffe');
    user.save();
    user = User.objects.create_user('bee', '', 'bee');
    user.save();
    user = User.objects.create_user('eagle', '', 'eagle');
    user.save();

    # group 9
    user = User.objects.create_user('deer', '', 'deer');
    user.save();
    user = User.objects.create_user('penguin', '', 'penguin');
    user.save();


    #group 10
    user = User.objects.create_user('alligator', '', 'alligator');
    user.save();
    user = User.objects.create_user('raccoon', '', 'raccoon');
    user.save();
    user = User.objects.create_user('lion', '', 'lion');
    user.save()


    #group 11 - teacher/developers
    user = User.objects.create_user('AW', '', 'AW');
    user.save();
    user = User.objects.create_user('user1', '', 'user1');
    user.save();
    user = User.objects.create_user('user2', '', 'user2');
    user.save();


    return HttpResponse('')



# hacks - end

def dataToCSV(request):
    #get all the image objects and serialize to get the foreign key values
    sql = imageModel.objects.all();
    sql = serializers.serialize('json', sql, use_natural_foreign_keys=True)

    # how many image posted by each user?
    sql = imageModel.objects.values('posted_by_id').annotate(dcount=Count('posted_by_id'))
    # TODO: unable to serialize this query with the following
    #sql = serializers.serialize('json', sql, use_natural_foreign_keys=True)

    #get imagecomment count grouped by image id but does not give the content
    sql = imageComment.objects.values('imageId_id').annotate(dcount=Count('imageId_id'))
    #print(sql) #print the result #print(len(sql[0]) #prints 2 - length of the first element
    print(len(sql)) #get the length of total image group by count

    #get distinct image id from imagecomment model
    #https://stackoverflow.com/questions/10848809/django-model-get-distinct-value-list
    sql = imageComment.objects.order_by('imageId_id').values('imageId_id').distinct()

    #get the distinct image id in a list
    image_id_list = [query['imageId_id'] for query in sql]
    print(image_id_list)

    #only get the content field for each image id
    #http://books.agiliq.com/projects/django-orm-cookbook/en/latest/select_some_fields.html
    imageContent = []
    for image_id in image_id_list:
        #print(imageComment.objects.filter(imageId_id = image_id).values('content'))
        comments = imageComment.objects.filter(imageId_id = image_id).values('content','posted_by_id')
        # convert the query set into a list -- list(comments)
        #process comments to remove content from each row
        # #https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json
        #comment_list = json.dumps([dict(item) for item in comments])
        comment_list = [dict(item) for item in comments]
        #print(comment_list)

        #print(list(comments))
        item = {}
        item['imageID'] = image_id
        item['comments'] = comment_list
        imageContent.append(item)


    print(json.dumps(imageContent))
    return HttpResponse('')

def perUserDataExtract(request):
    #get all the user list
    users_list = [str(user) for user in User.objects.all()]
    users_list.insert(0,0) #to start indexing from 1 instead of 0 to match user pk
    #print(users_list[1:])

    user_activity = []
    for user in users_list[1:29]:
        #get image comment
        #index and primary id is the same for user
        imagecomment = imageComment.objects.filter(posted_by_id = users_list.index(user)).order_by('imageId_id').values('content','imageId_id')
        comment_list = [dict(item) for item in imagecomment]

        item = {}
        item['userID'] = users_list.index(user)
        item['imagecomment'] = comment_list

        #get activity feed message for each user
        general_chat_message = Message.objects.filter(posted_by_id = users_list.index(user)).values('content')
        general_chat_message = [gcm['content'] for gcm in general_chat_message]
        item['generalmessage'] = general_chat_message
        user_activity.append(item)


    #print(json.dumps(user_activity))

    #https://stackoverflow.com/questions/42354001/python-json-object-must-be-str-bytes-or-bytearray-not-dict
    context = {'user_activity': json.loads(json.dumps(user_activity))}
    return render(request, 'app/studentList.html', context)

    #return HttpResponse('')

def getGeneralChatMsg(request):
    userid_list = [user['posted_by_id'] for user in Message.objects.values('posted_by_id').distinct()]
    generalChatComment_list = []
    for userid in userid_list:
        dict = {}
        dict[userid] = [item['content'] for item in Message.objects.filter(posted_by_id=userid).values('content')]
        generalChatComment_list.append(dict)

    return HttpResponse(generalChatComment_list)

def getimageCommentCount(request):
    imageComment_count = imageComment.objects.values('posted_by_id').annotate(dcount=Count('posted_by_id'))
    print(imageComment_count)

    # list of unique users who posted in khan academy (not all users may post in khan academy)
    userid_list = [user['posted_by_id'] for user in imageComment.objects.values('posted_by_id').distinct()]

    imageComment_list = []
    for userid in userid_list:
        dict = {}
        dict[userid] = [item['content'] for item in imageComment.objects.filter(posted_by_id=userid).values('content')]
        imageComment_list.append(dict)

    return HttpResponse(imageComment_list)

def getimageCommentDetails(request):
    # sort out images by each gallery id
    gallery_id = [gid['gallery_id'] for gid in imageModel.objects.values('gallery_id').distinct()];
    gallery_id.sort(); #in place sort, next time the list will be sorted.
    print(gallery_id);

    list = [] #list of dictionary items
    for gid in gallery_id:
        dict={}
        dict[gid] = [iid['id'] for iid in imageModel.objects.filter(gallery_id=gid).values('id')]
        list.append(dict);

    # print list of dictionary items in key/value pairs
    # for item in list:
    #     for k,v in item.items():
    #         print('{}: {}'.format(k,v));

    for item in list:
        for k,v in item.items():
            #v is the list of images in gallery k.
            print('gallery #', k, 'has',len(v),'images');
            print('image id list for gallery #', k, ':',v);
            for i in v:
                print('image id:',i, '---',imageComment.objects.filter(imageId_id=i).values('isGroupDiscussion').annotate(Count('isGroupDiscussion')))



    return HttpResponse();
def getkhanAcademyCount(request):
    khanacademy_count = khanAcademyAnswer.objects.values('posted_by_id').annotate(dcount=Count('posted_by_id'))
    #print(khanacademy_count)

    # list of unique users who posted in khan academy (not all users may post in khan academy)
    userid_list = [user['posted_by_id'] for user in khanAcademyAnswer.objects.values('posted_by_id').distinct()]

    kaResponse_list = []
    for userid in userid_list:
        dict = {}
        dict[userid] = [{'type':item['response_type'], 'response':item['response']} for item in khanAcademyAnswer.objects.filter(posted_by_id=userid).values('response_type', 'response')]
        kaResponse_list.append(dict)

    return HttpResponse(kaResponse_list)

def getKhanAcademyDetails(request):
    #get total post on each khan academy
    khanacademy_count = khanAcademyAnswer.objects.values('ka_id').annotate(dcount=Count('ka_id'))

    kid_list = [k['ka_id'] for k in khanAcademyAnswer.objects.values('ka_id').distinct()]

    list = [];
    for kid in kid_list:
        dict = {}
        dict[kid] = [{'userid':User.objects.get(pk=item['posted_by_id']).username, 'count':item['dcount']} for item in khanAcademyAnswer.objects.filter(ka_id=kid).values('posted_by_id').annotate(dcount=Count('posted_by_id'))]
        list.append(dict)


    return HttpResponse()


def getBadgeCount(request):
    #total count of badges each user recieved
    badge_count = badgeModel.objects.values('userid_id').annotate(dcount=Count('userid_id'));
    #print(badge_count);

    # identify different badges for each user
    #list of unique users who received badge (not all users may not get badge)
    userid_list = [user['userid_id'] for user in badgeModel.objects.values('userid_id').distinct()]
    #print(userid_list)

    # get  all of the badges for each user -- it will return dict in the format <userid:badgelist>
    badge_list = []
    for userid in userid_list:
        badge_dict = {}
        user = User.objects.get(pk=userid).username
        badge_dict[user] = [item['badgeType'] for item in badgeModel.objects.filter(userid_id=userid).values('badgeType')]
        badge_list.append(badge_dict)

    #print(badge_list)
    return HttpResponse(badge_list)

def getBadgeDetails(request):
    badge_list = badgeModel.objects.values('message','badgeType','userid_id');
    list=[];
    for item in badge_list:
        list.append(item)
    print(list)
    return HttpResponse(list)

def addUserToGroupsForm(request):
    return render(request, 'app/group.html', {})

def deleteAllItems(request):
    brainstormNote.objects.all().delete()
    imageModel.objects.all().delete()
    Message.objects.all().delete()
    random_group_users.objects.all().delete();
    #userLogTable.objects.all().delete();
    khanAcademyAnswer.objects.all().delete();
    # groupInfo.objects.all().delete()

    return HttpResponse('')

def getAllUserList():
    users_list = [str(user) for user in User.objects.all()]

    return users_list;