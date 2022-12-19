from django.db import models


class UserChoices(models.Model):
    class Priorities(models.IntegerChoices):
        USELESS = 0
        HIGH = 1
        MEDIUM = 2
        LOW = 3

    class Validities(models.IntegerChoices):
        DAY = 1
        WEEK = 7
        MONTH = 30

    amount = models.IntegerField()
    validity = models.IntegerField(
        choices=Validities.choices,
        default=Validities.DAY
    )
    sms = models.IntegerField(
        choices=Priorities.choices,
        default=Priorities.USELESS
    )
    call = models.IntegerField(
        choices=Priorities.choices,
        default=Priorities.USELESS
    )
    datas = models.IntegerField(
        choices=Priorities.choices,
        default=Priorities.USELESS
    )
