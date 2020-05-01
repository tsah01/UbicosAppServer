
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login_form, name='login_form'),
    url('login', views.login, name='login'),
    url('logout', auth_views.LogoutView.as_view()),
    url('index', views.index, name='index'),

# My work starts from here(Tula)
    url('teacher', views.teacher, name='teacher'),
    url('home', views.home, name='home'),
    url('ratio', views.ratio, name='ratio'),
    url('volumeAndSurface', views.volumeAndSurface, name='volumeAndSurface'),
    url('linearFunction', views.linearFunction, name='linearFunction'),
    url('studentProfile', views.studentProfile, name='studentProfile'),


    url('getUsername', views.getUsername),
    url('getGroupID/(?P<act_id>\d+)', views.getGroupID),
    url('getUserList',views.getUserList),
    url('studentID/(?P<std_id>\d+)',views.getAllStudentInfo),
    url('createUser',views.createUser),
    url('createBulkUser',views.createBulkUser),
    url('addUserToGroups',views.addUserToGroupsForm),
    url('registerUser',views.registerUser),
    url('groupAdd', views.groupAdd),
    #urls for different tool utility
    url('uploadImage', views.uploadImage, name='uploadImage'),
    url('getImage/(?P<view_id>\d+)/(?P<gallery_id>\d+)/(?P<group_id>\d+)/', views.getImage, name='getImg'),
    url('getImageID/(?P<img_filename>[\w+._^%$#!~@,-]+)/', views.getImageID), #regular expression checker: https://regex101.com/r/iQ8gG4/1
    url('getImagePerUser/(?P<act_id>\d+)/(?P<username>[\w+._^%$#!~@,-]+)/', views.getImagePerUser), #regular expression checker: https://regex101.com/r/iQ8gG4/1
    url(r'^ajax/imageComment/$', views.broadcastImageComment),
    url('updateImageFeed/(?P<img_id>\d+)', views.updateImageFeed),
    url('gallery/del/(?P<img_id>\d+)', views.imageDelete),
    url('getGalleryPerID/(?P<gid>\d+)', views.getGalleryPerID),
    url('getRandomGroupMemberList/(?P<gallery_id>\d+)', views.getRandomGroupMemberList),
    #url('brainstorm/save/',views.brainstormSave),
    url('brainstorm/save/',views.broadcastBrainstormNote),
    url('brainstorm/get/(?P<brainstorm_id>\d+)',views.brainstormGet),
    url('brainstorm/update/(?P<note_id>\d+)/', views.brainstormUpdate),
    url('brainstorm/del/(?P<note_id>\d+)', views.brainstormDelete),
    url(r'^ajax/chat/$', views.broadcast),
    url('updateFeed/(?P<type>\d+)', views.updateFeed),
    url('tableData/save/',views.tableEntriesSave),
    url('submitAnswer',views.submitAnswer),
    url('uploadKAImage', views.uploadKAImage),
    url('submitKAAnswer',views.submitKAAnswer),
    url('getKAPerKAID/(?P<ka_id>[0-9]+)',views.getKAPerKAID),
    url('checkKAAnswer/(?P<ka_id>\d+)',views.checkKAAnswer),
    url('dashboardKAInfo/(?P<ka_id>\d+)',views.dashboardKAInfo),
    #badges
    url('insertBadges',views.insertBadges),
    url('getBadges',views.getBadges),
    url('parser',views.pageParser),
    url('camera',views.camera),
    url('randomDiscussionGroupCreate',views.random_discussion_group_generator),
    url('getMediumGroupDiscussion',views.getMediumGroupDiscussion),
    url('updateDiscussionImageFeed/(?P<gallery_id>\d+)',views.updateDiscussionImageFeed),
    url('updateDiscussionImageFeedTeacherVersion/(?P<gallery_id>\d+)/(?P<group_id>\d+)/',views.updateDiscussionImageFeedTeacherVersion),
    url('getRandomListData/(?P<gallery_id>\d+)/(?P<group_id>\d+)/',views.getRandomListData),
    url('randomDiscussionList',views.randomDiscussionList),
    url('userlog', views.userlog),
    url(r'^extensionlog/$', views.userLogFromExtenstion),
    url('delete', views.deleteAllItems, name='activities'),
    #data analysis
    url('dataToCSV',views.dataToCSV),
    url('perUserDataExtract',views.perUserDataExtract),
    url('getBadgeCount',views.getBadgeCount),
    url('getBadgeDetails',views.getBadgeDetails),
    url('getimageCommentCount',views.getimageCommentCount),
    url('getimageCommentDetails',views.getimageCommentDetails),
    url('getGeneralChatMsg',views.getGeneralChatMsg),
    url('getkhanAcademyCount',views.getkhanAcademyCount),
    url('getKhanAcademyDetails',views.getKhanAcademyDetails),
    #teacherdashboard
    url('getGalleryTableTD/(?P<act_id>\d+)',views.getGalleryTableTD),
    url('dashboardGalleryInfo/(?P<act_id>\d+)',views.dashboardGalleryInfo),
    url('getDashboard',views.getDashboard),
    url('getGalleryPerID/(?P<gid>\d+)',views.getGalleryPerID)


]