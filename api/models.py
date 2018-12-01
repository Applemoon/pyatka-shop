from django.db import models


class Item(models.Model):
    MILK = 'milk'
    MEAT = 'meat'
    FRUITS = 'fruits'
    VEGETABLES = 'vegetables'
    CEREALS = 'cereals'
    SPICES = 'spices'
    OTHER = 'other'
    CATEGORY_CHOICES = (
        (MILK, 'молочка'),
        (MEAT, 'мясо, рыба, яйца'),
        (FRUITS, 'фрукты'),
        (VEGETABLES, 'овощи'),
        (CEREALS, 'крупы, макароны, хлеб'),
        (SPICES, 'приправы, майонез, кетчуп, соль, масло, сахар'),
        (OTHER, 'прочее: вода, кондитерка, алкоголь, химия'),
    )

    name = models.TextField(max_length=50)
    needed = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    bought = models.BooleanField(default=False)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=OTHER,
    )

    def __str__(self):
        return self.name

    def getDict(self):
        return {
            'name': self.name,
            'starred': self.starred,
            'id': self.id,
            'needed': self.needed,
            'bought': self.bought,
            'category': self.category
        }
