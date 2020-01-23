# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils import timezone
import pytz


#RankTank
#################################################################


class Account(models.Model): 
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20, default='o')
    is_admin = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.email


class Contest(models.Model): 
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title



class Contestant(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    contestant = models.CharField(max_length = 200)
    points = models.IntegerField(default=0)
    rank = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.contestant

    class Meta:
        ordering = ['rank']




class PrivateVoter(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    voter = models.CharField(max_length = 200)
    url = models.CharField(default=0, max_length = 100)
    is_vote = models.BooleanField(default=False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.voter

    class Meta:
        ordering = ['voter']







class ForgotPassword(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.reset_code