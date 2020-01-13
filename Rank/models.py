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
    firstname = models.CharField(max_length = 20, default='Oo')
    lastname = models.CharField(max_length = 20, default='Oo')
    is_admin = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return email


class Contest(models.Model): 
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return name



class Contestant(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    contestant = models.CharField(max_length = 200)
    points = models.IntegerField(default=0)
    rank = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return contestant

    class Meta:
        ordering = ['rank']




class PrivateVoter(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    voter = models.CharField(max_length = 200)
    url = models.CharField(default=0, max_length = 100)
    is_vote = models.BooleanField(default=False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return voter

    class Meta:
        ordering = ['voter']







class ForgotPassword(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return reset_code