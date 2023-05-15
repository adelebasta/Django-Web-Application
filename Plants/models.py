from django.db import models
from django.utils.timezone import now
from Useradmin.models import MyUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.core.exceptions import ValidationError



class Plant(models.Model):
    SUNLIGHT = [
        ("SU", "full sun"),
        ("SH", "full shade"),
        ("PS", "partial sun"),
    ]

    plant_picture = models.ImageField(upload_to='plant_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,
                                   blank=True)
    sunlight = models.CharField(max_length=2,
                                choices=SUNLIGHT)
    size = models.FloatField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='myusers',
                               related_query_name='myuser')
    timestamp = models.DateTimeField(blank=True,
                                     default=now)

    class Meta:
        ordering = ['timestamp', 'name']
        verbose_name = "Plant"
        verbose_name_plural = "Plants"

    def get_full_name(self):
        full_name = self.name
        if self.description:
            full_name += " / Sunlight: " + self.get_sunlight_display()
        return full_name

    def get_stars(self):
        average_rating = Comment.objects.filter(plant=self).aggregate(avg_rating=Avg('stars'))
        average_rating_values = ["star-dark2", "star-dark2", "star-dark2", "star-dark2", "star-dark2"]
        if average_rating['avg_rating'] is not None:
            for star in range(5):
                if star < int(round(average_rating['avg_rating'])):
                    average_rating_values[star] = "star"
            return average_rating_values
        else:
            return 0


    def __str__(self):
        return self.name + " (" + self.myuser.username + ")"

    def __repr__(self):
        return self.get_full_name() + " (" + self.myuser.username + ")"


class Comment(models.Model):

    stars = models.IntegerField(choices=list(zip(range(1, 6), range(1, 6))), default=5)
    text = models.TextField(max_length=300)
    timestamp = models.DateTimeField(blank=True,
                                     default=now)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant,
                              on_delete=models.CASCADE,
                              related_name='rated_plant',
                              related_query_name='rated_plant')
    is_reported = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_votes_count(self):
        u_votes = len(Vote.objects.filter(up_or_down='up',
                                    comment=self))
        d_votes = len(Vote.objects.filter(up_or_down='down',
                                      comment=self))
        return u_votes-d_votes


    def one_vote_per_user(self, myuser, up_or_down):
        user_vote = Vote.objects.filter(myuser=myuser,
                                        comment=self)
        if len(user_vote) == 0:
            Vote.objects.create(up_or_down=up_or_down,
                                myuser=myuser,
                                comment=self
                                )
        else:
            if user_vote[0].up_or_down == up_or_down:
                user_vote.delete()
            else:
                user_vote.delete()
                Vote.objects.create(up_or_down=up_or_down,
                                    myuser=myuser,
                                    comment=self
                                    )

    def is_reported_by_me(self, myuser):
        if len(Report.objects.filter(myuser=myuser, comment=self)) == 0:
            return False
        return True

    def get_stars(self):
        rating_values = ["star-dark2", "star-dark2", "star-dark2", "star-dark2", "star-dark2"]
        for star in range(5):
            if star < int(round(self.stars)):
                rating_values[star] = "star"
        return rating_values

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        return self.text

    def report(self, myuser):
        Report.objects.create(comment=self, myuser=myuser)
        self.is_reported = True
        self.save()

    def is_reported(self):
        if len(Report.objects.filter(comment=self)) > 0:
            return True
        return False

    def clear_report(self):
        Report.objects.filter(comment=self.id).delete()
        self.is_reported = False
        self.save()

    def __str__(self):
        return self.get_comment_prefix() + '(' + self.myuser.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + '(' + self.myuser.username + '/' + str(self.timestamp) + ')'


class Vote(models.Model):

    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down')
    ]
    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES)
    timestamp = models.DateTimeField(blank=True,
                                     default=now)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return self.get_up_or_down_display() + ' on ' + self.comment.id + ' by ' + self.myuser.username + ')'


class Report(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment.__str__() + ' was reported by ' + self.myuser.name + ' on ' + self.timestamp