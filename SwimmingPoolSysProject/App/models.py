from django.db import models
import datetime
from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=45, null=False)
    surname = models.CharField(max_length=45, null=False)
    phoneNumber = models.CharField(max_length=9, null=False)
    email = models.EmailField(null=True)
    pesel = models.CharField(max_length=11, null=False)

    def __str__(self):
        return f'{self.name} {self.surname}'


class WorkerAddress(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, default=None)
    street = models.CharField(max_length=45, null=False)
    houseNumber = models.IntegerField(null=False)
    flatNumber = models.IntegerField(null=True)
    postcode = models.CharField(max_length=11, null=False)
    placeName = models.CharField(max_length=45, null=False)

    def __str__(self):
        return f'{self.worker}'


class Shift(models.Model):

    SHIFTS_CHOICES = (
        ("1 zmiana", "1 zmiana"),
        ("2 zmiana", "2 zmiana")
    )

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, default=None)
    startTime = models.DateTimeField(null=False)
    endTime = models.DateTimeField(null=True, blank=True, editable=False)
    description = models.CharField(max_length=12, choices=SHIFTS_CHOICES)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.endTime = self.startTime + datetime.timedelta(hours=8)
        super(Shift, self).save(*args, **kwargs)

    def __str__(self):
        return self.description


class Client(models.Model):
    name = models.CharField(max_length=45, null=False)
    surname = models.CharField(max_length=45, null=False)
    phoneNumber = models.CharField(max_length=9, null=False)
    email = models.EmailField(null=True)
    pesel = models.CharField(max_length=11, null=False)

    def __str__(self):
        return f'{self.name} {self.surname}'


class ClientAddress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    street = models.CharField(max_length=45, null=False)
    houseNumber = models.IntegerField(null=False)
    flatNumber = models.IntegerField(null=True, blank=True)
    postcode = models.CharField(max_length=11, null=False)
    placeName = models.CharField(max_length=45, null=False)

    def __str__(self):
        return f'{self.client}'


class Ticket(models.Model):

    TICKET_CHOICES = (
        ("Pływalnia", "Pływalnia"),
        ("SPA", "SPA"),
        ("Siłownia", "Siłownia"),
    )

    worker = models.ForeignKey(Worker, on_delete=models.SET_DEFAULT, default=None)
    client = models.ForeignKey(Client, on_delete=models.SET_DEFAULT, default=None)
    price = models.FloatField(null=False)
    zone = models.CharField(max_length=45, null=False, choices=TICKET_CHOICES)
    dateOfPurchase = models.DateTimeField(null=False, default=datetime.datetime.now(), editable=False)
    dateOfEnd = models.DateTimeField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.dateOfEnd = self.dateOfPurchase + datetime.timedelta(hours=1)
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.client}'