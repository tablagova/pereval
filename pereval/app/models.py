from django.db import models


ADDED_STATUS = [
    ('new', 'новая заявка'),
    ('pending', 'заявка рассматривается'),
    ('accepted', 'данные приняты'),
    ('rejected', 'данные не приняты'),
]


class Users(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=25)
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=25)
    otc = models.CharField(max_length=25)

    class Meta:
        db_table = 'pereval_user'


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    class Meta:
        db_table = 'pereval_coords'


class PerevalAdded(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255, blank=True)
    add_time = models.DateTimeField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE)
    winter_level = models.CharField(max_length=10, blank=True)
    summer_level = models.CharField(max_length=10, blank=True)
    autumn_level = models.CharField(max_length=10, blank=True)
    spring_level = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=50, choices=ADDED_STATUS, default=ADDED_STATUS[0])

    class Meta:
        db_table = 'pereval_added'


class Images(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=20)
    img = models.BinaryField()
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pereval_images'
