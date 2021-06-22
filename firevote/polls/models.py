from django.db import models

# Create your models here.

class Positions(models.Model):
    positn_name = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = 'Positions'

class Candidates(models.Model):
    candid_name = models.CharField(max_length=50)
    candid_posn = models.CharField( max_length= 50)
    votes = models.PositiveIntegerField( default=0 )

    class Meta:
        verbose_name_plural = 'Candidates'

class Admin(models.Model):
    admin_name = models.CharField(max_length=20)
    admin_passwd = models.CharField(max_length=20)

class Voters(models.Model):
    voter_name = models.CharField(max_length= 50)
    voter_id = models.CharField(max_length=10)
    voter_passwd = models.CharField(max_length=20)
    voter_num = models.CharField(max_length=10, default= '8959636987', primary_key=True)
    voter_permit = models.CharField(max_length=3, default = 'no' , choices=(("yes","Yes"),("no","No")))

    def __str__(self):
        return self.voter_name+'('+self.voter_num+')'

    class Meta:
        verbose_name_plural = 'Voters'

class Record(models.Model):
    voter_name = models.CharField(max_length=50)
    vote_posn = models.CharField(max_length= 50)