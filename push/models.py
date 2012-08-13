from django.db import models

class FoursquareUser(models.Model):
    userId = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    photo = models.CharField(max_length=200)
    gender = models.CharField(max_length=6)
    homeCity = models.CharField(max_length=100)
    bio = models.TextField()
    twitter = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        string = "%s %s" % (self.firstName, self.lastName)
        return string

class Venue(models.Model):
    venueId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100)
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    postalCode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    categoryId = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    categoryPluralName = models.CharField(max_length=100)
    categoryShortName = models.CharField(max_length=100)
    categoryIcon = models.CharField(max_length=200)
    categoryPrimary = models.BooleanField()
    statsCheckinsCount = models.IntegerField()
    statsUsersCount = models.IntegerField()
    statsTipsCount = models.IntegerField()
    statsLikesCount = models.IntegerField()
    url = models.URLField()
    mayor = models.ForeignKey('FoursquareUser',blank=True)
    venueLogo = models.ImageField(upload_to='venue/logos')

    def __unicode__(self):
        string = "%s (%s)" % (self.name, self.address)
        return string

class Checkin(models.Model):
    checkinId = models.CharField(max_length=100)
    createdAt = models.DateTimeField()
    timezone = models.CharField(max_length=50)
    user = models.ForeignKey('FoursquareUser')
    venue = models.ForeignKey('Venue')

    def time_ago(self):
        from datetime import datetime
        now = datetime.now()
        diff = now - self.createdAt
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return  "a minute ago"
            if second_diff < 3600:
                return str( second_diff / 60 ) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str( second_diff / 3600 ) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(day_diff/7) + " weeks ago"
        if day_diff < 365:
            return str(day_diff/30) + " months ago"
        return str(day_diff/365) + " years ago"

    def __unicode__(self):
        string = "%s by %s %s" % (self.checkinId, self.user.firstName, self.user.lastName)
        return string