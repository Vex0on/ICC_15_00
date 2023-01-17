from django.db import models
import datetime


class Worker(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=9, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    pesel = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class WorkerAddress(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    street = models.CharField(max_length=45)
    houseNumber = models.IntegerField()
    flatNumber = models.IntegerField(null=True, blank=True)
    postcode = models.CharField(max_length=11)
    placeName = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.worker}'


class Shift(models.Model):

    SHIFTS_CHOICES = (
        ("1 zmiana", "1 zmiana"),
        ("2 zmiana", "2 zmiana")
    )

    worker = models.ManyToManyField(Worker)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField(null=True, blank=True, editable=False)
    description = models.CharField(max_length=12, choices=SHIFTS_CHOICES)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.endTime = self.startTime + datetime.timedelta(hours=8)
        super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class Client(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=9, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    pesel = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class ClientAddress(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    street = models.CharField(max_length=45)
    houseNumber = models.IntegerField()
    flatNumber = models.IntegerField(null=True, blank=True)
    postcode = models.CharField(max_length=11)
    placeName = models.CharField(max_length=45)

    def __str__(self):
        return f'{self.client}'


class Ticket(models.Model):

    ZONE_CHOICES = (
        ("Pływalnia", "Pływalnia"),
        ("SPA", "SPA"),
        ("Siłownia", "Siłownia")
    )

    PRICE_CHOICES = (
        ('19.99', '19.99zł'),
        ('25', '25zł'),
        ('33', '33zł')
    )

    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    price = models.CharField(max_length=6, choices=PRICE_CHOICES)
    zone = models.CharField(max_length=45, choices=ZONE_CHOICES)
    dateOfPurchase = models.DateTimeField(default=datetime.datetime.now(), editable=False)
    dateOfEnd = models.DateTimeField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.dateOfEnd = self.dateOfPurchase + datetime.timedelta(hours=1)
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.zone}'