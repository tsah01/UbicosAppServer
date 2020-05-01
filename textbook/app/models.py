from django.db import models
from django.conf import settings
import jsonfield


# Create your models here.
class ActivityIndex(models.Model):
    page_number = models.IntegerField()
    activity_type = models.CharField(max_length=40)


class imageModel(models.Model):

    gallery_id = models.IntegerField()
    group_id = models.IntegerField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images')

    class Meta:
        unique_together = (('posted_by', 'id'),)

    #https://docs.djangoproject.com/en/2.0/topics/serialization/
    #https://stackoverflow.com/questions/28591176/serializing-django-model-and-including-further-information-for-foreignkeyfield
    def natural_key(self):
        #return (self.posted_by.username)
        return (self.id)


class imageComment(models.Model):
    content = models.CharField(max_length=400)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    imageId = models.ForeignKey(imageModel, on_delete=models.CASCADE)
    isGroupDiscussion = models.CharField(max_length=400)

    def natural_key(self):
        return (self.posted_by.username)

class khanAcademyAnswer(models.Model):
    ka_id = models.IntegerField()
    ka_image = models.ImageField(upload_to='ka_images')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    response_type = models.CharField(max_length=20)
    response = models.CharField(max_length=2000)

    def natural_key(self):
        return (self.posted_by.username)

# activity feed message
class Message(models.Model):
    content = models.CharField(max_length=400)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def natural_key(self):
        return (self.posted_by.username)

class badgeModel(models.Model):
    userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=400)
    badgeType = models.CharField(max_length=400)
    platform = models.CharField(max_length=10)


    def natural_key(self):
        return (self.userid.username)


class brainstormNote(models.Model):
    brainstormID = models.IntegerField(null=True)
    ideaText = models.CharField(max_length=400)
    color = models.CharField(max_length=20)
    position_top = models.CharField(max_length=20)
    position_left = models.CharField(max_length=20)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def natural_key(self):
        return (self.posted_by.username)

class tableChartData(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table_id = models.IntegerField(null=True)
    plot_type = models.CharField(max_length=20) #enumeration
    plot_data = jsonfield.JSONField() #https://stackoverflow.com/questions/37007109/django-1-9-jsonfield-in-models

class userQuesAnswerTable(models.Model):
    questionIDbyPage = models.IntegerField(null=True)
    answer = jsonfield.JSONField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

#temp solution for pilot-1 -- start
class groupInfo(models.Model):
    activityType = models.CharField(max_length=20)
    activityID = models.IntegerField(null=True)
    group = models.IntegerField(null=True)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.activityID, self.group)
#temp solution for pilot-1 -- end

class random_group_users(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gallery_id = models.IntegerField()
    group = models.CharField(max_length=20)

    def natural_key(self):
        return (self.posted_by.username)

class userLogTable(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    type = models.CharField(max_length=200)
    input = models.CharField(max_length=200)
    pagenumber = models.IntegerField(null=True)
    posted_at = models.DateTimeField(auto_now_add=True)


class topics(models.Model):
    topic_name = models.CharField(max_length=20)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityIndex, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_name

class modelbook(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    topic = models.ForeignKey(topics, on_delete=models.CASCADE)
    activities = models.ForeignKey(ActivityIndex, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class colorcode(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #color_type = models.ColorField('#ffffff')
    activities = models.ForeignKey(ActivityIndex, on_delete=models.CASCADE)

