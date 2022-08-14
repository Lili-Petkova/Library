from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField("date of birth", null=True, blank=True)
    date_of_death = models.DateField("date of death", null=True, blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    pubdate = models.DateField()

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField('Book')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    store = models.ManyToManyField('Store')

    def __str__(self):
        return self.name
