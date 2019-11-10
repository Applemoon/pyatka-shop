from django.db import models


def incrementPosition():
    return Category.objects.count()


class Category(models.Model):
    # Unique 'name' has some advantages over pk:
    # - it's obvious to debag requests
    # - it's obvious to manage category on admin pages
    # - we can just write the name to classes and make css dependences on them
    # - it's easier to define default category
    name = models.CharField(max_length=20, unique=True, default='other')
    full_name = models.CharField(max_length=200)
    position = models.PositiveSmallIntegerField(default=incrementPosition)

    def __str__(self):
        return self.full_name

    def items_count(self):  # for admin page
        return self.item_set.count()


def getDefaultCategory():
    default_name = Category._meta.get_field('name').get_default()
    try:
        return Category.objects.get(name=default_name)
    except Category.DoesNotExist:
        return Category.objects.create(
            name=default_name,
            full_name=default_name
        )


class Item(models.Model):
    name = models.CharField(max_length=1000)
    needed = models.BooleanField(default=False)
    bought = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=getDefaultCategory,
    )

    def __str__(self):
        return self.name
