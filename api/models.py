from django.db import models


def incrementPosition():
    return Category.objects.count()


def getDefaultCategory():
    try:
        return Category.objects.get(name=Category.default_name).id
    except Category.DoesNotExist:
        return Category.objects.create(
            name=Category.default_name,
            full_name=Category.default_name,
        )


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    position = models.PositiveSmallIntegerField(default=incrementPosition)

    default_name = 'other'

    def __str__(self):
        return self.full_name

    def getDict(self):
        return {
            'name': self.name,
            'full_name': self.full_name,
            'position': self.position,
        }

    def items_count(self):  # for admin page
        return self.item_set.count()


class Item(models.Model):
    name = models.CharField(max_length=50)
    needed = models.BooleanField(default=False)
    bought = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=getDefaultCategory,
    )

    def __str__(self):
        return self.name

    def getDict(self):
        return {
            'name': self.name,
            'id': self.id,
            'needed': self.needed,
            'bought': self.bought,
            'category': self.category.name,
        }
