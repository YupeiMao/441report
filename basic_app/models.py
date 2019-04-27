

from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
#User
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(null=True,blank=True)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user.username

#Company
class Company(models.Model):
    cid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
#User habits
class UserProperties(models.Model):
    uid = models.ForeignKey(UserProfileInfo, on_delete=models.PROTECT,null=True)
    overall_ratings = models.IntegerField(null=True,blank=True)
    work_balance_stars = models.IntegerField(null=True,blank=True)
    culture_values_stars = models.IntegerField(null=True,blank=True)
    career_opportunities_stars = models.IntegerField(null=True,blank=True)
    company_benefit_stars = models.IntegerField(null=True,blank=True)
    senior_management_stars = models.IntegerField(null=True,blank=True)

#Position
class Position(models.Model):
    pid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

#Review
class Review(models.Model):
    rid = models.IntegerField(primary_key=True)
    cid = models.ForeignKey(Company, on_delete=models.PROTECT)
    pid = models.ForeignKey(Position, on_delete=models.PROTECT)
    uid = models.ForeignKey(UserProfileInfo, on_delete=models.PROTECT)
    date = models.DateField()
    summary = models.TextField(null=True)
    pros = models.TextField(null=True)
    cons = models.TextField(null=True)
    advices_to_management = models.TextField(null=True)
    overall_ratings = models.CharField(max_length=10)
    work_balance_stars = models.CharField(max_length=10)
    culture_values_stars = models.CharField(max_length=10)
    career_opportunities_stars = models.CharField(max_length=10)
    company_benefit_stars = models.CharField(max_length=10)
    senior_management_stars = models.CharField(max_length=10)
    helpful_count = models.IntegerField()

class DeleteID(models.Model):
    did = models.IntegerField()
class EditID(models.Model):
    eid = models.IntegerField()
    summary = models.TextField(null=True)
class AddID(models.Model):
    cid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100,null=True)
    country = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)

class Images(models.Model):
    image = models.ImageField(upload_to='background_image', blank=True,null=True)

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255)
    pub_date = models.DateField()

    def __str__(self):
        return self.text

    def user_can_vote(self, user):
        """
        Returns False is user has already voted, else True
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def num_votes(self):
        return self.vote_set.count()

    def get_results_dict(self):
        """
        Returns a list of objects in the form:
        [
            # for each related choice
            {
                'text': choice_text,
                'num_votes': number of votes on that choice
                'percentage': num_votes / poll.num_votes * 100
            }
        ]
        """
        res = []
        for choice in self.choice_set.all():
            d = {}
            d['text'] = choice.choice_text
            d['num_votes'] = choice.num_votes
            if not self.num_votes:
                d['percentage'] = 0
            else:
                d['percentage'] = choice.num_votes / self.num_votes * 100
            res.append(d)
        return res


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.poll.text[:25], self.choice_text[:25])

    @property
    def num_votes(self):
        return self.vote_set.count()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
