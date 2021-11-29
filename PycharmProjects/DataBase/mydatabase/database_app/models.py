from django.db import models


# Create your models here.
class appuser(models.Model):
    objects = models.Manager()
    u_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class records(models.Model):
    r_id = models.IntegerField(primary_key=True)
    objects = models.Manager()
    r_date_time = models.DateTimeField()

    def __str__(self):
        return self.r_date_time


class schedule(models.Model):  # 该字段记录了用户的行程
    objects = models.Manager()
    s_id = models.IntegerField(primary_key=True)
    s_schedule = models.TextField()
    s_date = models.DateField()


class photo(models.Model):
    objects = models.Manager()
    r = models.ForeignKey("records", on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/%Y/%m/%d/')


class usertext(models.Model):
    objects = models.Manager()
    r = models.ForeignKey("records", on_delete=models.CASCADE)
    title = models.CharField(primary_key=True,max_length=128, default="每日好心情")
    text = models.TextField()


class save_s(models.Model):
    objects = models.Manager()
    s = models.ForeignKey("schedule", on_delete=models.CASCADE)
    u = models.ForeignKey("appuser", on_delete=models.CASCADE)

class save_r(models.Model):
    objects = models.Manager()
    u = models.ForeignKey("appuser", on_delete=models.CASCADE)
    r = models.ForeignKey("records",on_delete=models.CASCADE)