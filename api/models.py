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
        (MILK, 'Молочка'),
        (MEAT, 'Мясо, рыба, яйца'),
        (FRUITS, 'Фрукты'),
        (VEGETABLES, 'Овощи'),
        (CEREALS, 'Крупы, макароны, хлеб'),
        (SPICES, 'Приправы, майонез, кетчуп, соль, масло, сахар'),
        (OTHER, 'Прочее: вода, кондитерка, алкоголь, химия'),
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

    @staticmethod
    def getCategories():
        return [{'key': key, 'value': value}
                for key, value in Item.CATEGORY_CHOICES]
