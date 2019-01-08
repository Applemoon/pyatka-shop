from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from random import randrange

from .models import Category, Item


default_item = {
    'name': '',
    'needed': False,
    'bought': False,
    'category': 'other',
}
test_user = {
    'username': 'john',
    'email': 'lennon@thebeatles.com',
    'password': 'lennon_pass',
}


def getCategory():
    if Category.objects.count() == 0:
        return Category.objects.create(
            name=default_item['category'],
            full_name='This is a test category'
        )

    return Category.objects.first()


def createItem(
    name,
    needed=default_item['needed'],
    bought=default_item['bought']
):
    return Item.objects.create(
        name=name,
        needed=needed,
        bought=bought,
        category=getCategory()
    )


class CategoriesTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_categories(self):
        self.client.login(**test_user)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_call_categories_with_empty(self):
        response_arr = self.call_categories()
        self.assertEqual(len(response_arr), 0)

    def test_call_categories_not_empty(self):
        [Category.objects.create(
            name='test' + str(i), full_name='Test category ' + str(i))
            for i in range(2, randrange(3, 20))]
        init_categories_count = Category.objects.count()

        response_arr = self.call_categories()
        self.assertEqual(len(response_arr), Category.objects.count())
        self.assertEqual(len(response_arr), init_categories_count)

    def test_call_categories_not_logged_in(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 403)

    def test_call_categories_post_method(self):
        self.client.login(**test_user)

        response = self.client.post(reverse('category-list'))
        self.assertEqual(response.status_code, 405)


class ItemsGetTests(APITestCase):
    def setUp(self):
        Category.objects.create(
            name=default_item['category'],
            full_name='Test category'
        )
        User.objects.create_user(**test_user)

    def call_items_get(self):
        self.client.login(**test_user)
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_items_get_with_empty(self):
        response_arr = self.call_items_get()
        self.assertEqual(len(response_arr), 0)

    def test_items_get_not_empty(self):
        [createItem(name) for name in 'test' + str(randrange(2, 20))]
        init_items_count = Item.objects.count()

        response_arr = self.call_items_get()
        self.assertEqual(len(response_arr), Item.objects.count())
        self.assertEqual(len(response_arr), init_items_count)
        for resp_item in response_arr:
            item = Item.objects.get(pk=resp_item['id'])
            self.assertEqual(item.name, resp_item['name'])
            self.assertEqual(item.needed, resp_item['needed'])
            self.assertEqual(item.bought, resp_item['bought'])

    def test_items_get_not_logged_in(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 403)


class ItemsPostTests(APITestCase):
    def setUp(self):
        Category.objects.create(
            name=default_item['category'],
            full_name='Test category'
        )
        User.objects.create_user(**test_user)

    def call_items_post(self, data):
        self.client.login(**test_user)
        response = self.client.post(reverse('item-list'), data)
        self.assertEqual(response.status_code, 201)
        return response.data

    def test_create_default_item(self):
        name = 'test'
        data = {'name': name}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], default_item['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], default_item['category'])
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_with_category(self):
        name = 'test'
        category_2 = Category.objects.create(
            name='test 2',
            full_name='Test category 2'
        )
        data = {'name': name, 'category': category_2.name}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], default_item['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], category_2.name)
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_with_category_and_needed(self):
        name = 'test'
        category_2 = Category.objects.create(
            name='test 2',
            full_name='Test category 2'
        )
        data = {'name': name, 'category': category_2.name, 'needed': 'true'}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], name)
        self.assertTrue(response_dict['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], category_2.name)
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_with_category_and_not_needed(self):
        name = 'test'
        category_2 = Category.objects.create(
            name='test 2',
            full_name='Test category 2'
        )
        data = {'name': name, 'category': category_2.name, 'needed': 'false'}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], name)
        self.assertFalse(response_dict['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], category_2.name)
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_needed_item(self):
        self.client.login(**test_user)
        name = 'test'
        data = {'name': name, 'needed': 'true'}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], True)
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], default_item['category'])
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_not_needed_item(self):
        self.client.login(**test_user)
        name = 'test'
        data = {'name': name, 'needed': 'false'}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], False)
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], default_item['category'])
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_item_with_empty_data(self):
        self.client.login(**test_user)
        data = {}
        init_items_count = Item.objects.count()

        response_dict = self.call_items_post(data)
        self.assertEqual(response_dict['name'], default_item['name'])
        self.assertEqual(response_dict['needed'], default_item['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], default_item['category'])
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_item_with_wrong_needed(self):
        self.client.login(**test_user)
        data = {'name': 'test', 'needed': 'test2'}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('item-list'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_create_item_with_long_name(self):
        self.client.login(**test_user)
        name = 'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23'
        data = {'name': name}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('item-list'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_create_item_with_wrong_category(self):
        self.client.login(**test_user)
        data = {'name': 'test', 'category': 'wrong'}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('item-list'), data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_items_get_not_logged_in(self):
        data = {'name': 'test'}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('item-list'), data=data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_items_put_method(self):
        self.client.login(**test_user)
        name = 'test'
        data = {'name': name}
        init_items_count = Item.objects.count()

        response = self.client.put(reverse('item-list'), data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Item.objects.count(), init_items_count)


class SetNeededTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_set_needed(self, itemId):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[itemId]),
            data={'needed': True}
        )
        self.assertEqual(response.status_code, 200)

    def test_set_needed_default(self):
        item = createItem('test')

        self.call_set_needed(item.id)
        self.assertTrue(Item.objects.get(pk=item.id).needed)

    def test_set_needed_needless(self):
        item = createItem('test', needed=False)

        self.call_set_needed(item.id)
        self.assertTrue(Item.objects.get(pk=item.id).needed)

    def test_set_needed_needed(self):
        item = createItem('test', needed=True)

        self.call_set_needed(item.id)
        self.assertTrue(Item.objects.get(pk=item.id).needed)

    def test_set_needed_not_logged_in(self):
        item = createItem('test')

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={'needed': True}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(item.needed, default_item['needed'])

    def test_set_needed_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[0]),
            data={'needed': True}
        )
        self.assertEqual(response.status_code, 404)


class SetNotNeededTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_set_not_needed(self, itemId):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[itemId]),
            data={'needed': False}
        )
        self.assertEqual(response.status_code, 200)

    def test_set_not_needed_default(self):
        item = createItem('test')

        self.call_set_not_needed(item.id)
        self.assertFalse(Item.objects.get(pk=item.id).needed)

    def test_set_not_needed_needless(self):
        item = createItem('test', needed=False)

        self.call_set_not_needed(item.id)
        self.assertFalse(Item.objects.get(pk=item.id).needed)

    def test_set_not_needed_needed(self):
        item = createItem('test', needed=True)

        self.call_set_not_needed(item.id)
        self.assertFalse(Item.objects.get(pk=item.id).needed)

    def test_set_not_needed_not_logged_in(self):
        item = createItem('test')

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={'needed': False}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(item.needed, default_item['needed'])

    def test_set_not_needed_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[0]),
            data={'needed': False}
        )
        self.assertEqual(response.status_code, 404)


class SetBoughtTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_set_bought(self, itemId):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[itemId]),
            data={'bought': True}
        )
        self.assertEqual(response.status_code, 200)

    def test_set_bought_default(self):
        item = createItem('test')

        self.call_set_bought(item.id)
        self.assertTrue(Item.objects.get(pk=item.id).bought)

    def test_set_bought_not_bought(self):
        item = createItem('test', needed=False)

        self.call_set_bought(item.id)
        self.assertTrue(Item.objects.get(pk=item.id).bought)

    def test_set_bought_needed(self):
        item = createItem('test', needed=True)

        self.call_set_bought(item.id)
        self.assertTrue(Item.objects.get(pk=item.id).bought)

    def test_set_bought_not_logged_in(self):
        item = createItem('test')

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={'bought': True}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(item.bought, default_item['bought'])

    def test_set_bought_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[0]),
            data={'bought': True}
        )
        self.assertEqual(response.status_code, 404)


class SetNotBoughtTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_set_not_bought(self, itemId):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[itemId]),
            data={'bought': False}
        )
        self.assertEqual(response.status_code, 200)

    def test_set_not_bought_default(self):
        item = createItem('test')

        self.call_set_not_bought(item.id)
        self.assertFalse(Item.objects.get(pk=item.id).bought)

    def test_set_not_bought_not_bought(self):
        item = createItem('test', needed=False)

        self.call_set_not_bought(item.id)
        self.assertFalse(Item.objects.get(pk=item.id).bought)

    def test_set_not_bought_needed(self):
        item = createItem('test', needed=True)

        self.call_set_not_bought(item.id)
        self.assertFalse(Item.objects.get(pk=item.id).bought)

    def test_set_not_bought_not_logged_in(self):
        item = createItem('test')

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={'bought': False}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(item.bought, default_item['bought'])

    def test_set_not_bought_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[0]),
            data={'bought': False}
        )
        self.assertEqual(response.status_code, 404)


class SetAllNotBoughtTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_set_all_not_bought(self):
        self.client.login(**test_user)
        response = self.client.patch(reverse('item-all-not-bought'))
        self.assertEqual(response.status_code, 200)

    def test_set_all_not_bought_default(self):
        createItem('test', bought=True)
        createItem('test', bought=True)
        createItem('test', bought=False)
        createItem('test', bought=False)

        self.call_set_all_not_bought()
        for item in Item.objects.all():
            self.assertFalse(item.bought)

    def test_set_all_not_bought_nothing(self):
        createItem('test', bought=False)
        createItem('test', bought=False)
        createItem('test', bought=False)
        createItem('test', bought=False)

        self.call_set_all_not_bought()
        for item in Item.objects.all():
            self.assertFalse(item.bought)

    def test_set_all_not_bought_empty(self):
        self.call_set_all_not_bought()
        self.assertEqual(Item.objects.count(), 0)

    def test_set_all_not_bought_not_logged_in(self):
        items = [
            createItem('test', bought=True),
            createItem('test', bought=True),
            createItem('test', bought=True),
            createItem('test', bought=True),
        ]

        response = self.client.post(reverse('item-all-not-bought'))
        self.assertEqual(response.status_code, 403)
        for item in items:
            self.assertTrue(item.bought)

    def test_set_all_not_bought_get_method(self):
        self.client.login(**test_user)
        createItem('test', bought=True)

        response = self.client.get(reverse('item-all-not-bought'))
        self.assertEqual(response.status_code, 405)


class RemoveTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_remove_item(self, item_id):
        self.client.login(**test_user)
        response = self.client.delete(reverse('item-detail', args=[item_id]))
        self.assertEqual(response.status_code, 204)

    def test_remove_default_item(self):
        item = createItem('test')

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_last_item(self):
        item = createItem('test1')
        createItem('test2')

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 1)
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=item.id)

    def test_remove_needed_item(self):
        item = createItem('test', needed=True)

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_needed_item(self):
        item = createItem('test', needed=False)

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_bought_item(self):
        item = createItem('test', bought=True)

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_bought_item(self):
        item = createItem('test', bought=False)

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_item_with_empty_name(self):
        item = createItem('')

        self.call_remove_item(item.id)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_logged_in(self):
        item = createItem('test')

        response = self.client.delete(reverse('item-detail', args=[item.id]))
        self.assertEqual(response.status_code, 403)

    def test_remove_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.delete(reverse('item-detail', args=[0]))
        self.assertEqual(response.status_code, 404)

    def test_double_remove(self):
        self.client.login(**test_user)
        item = createItem('test')
        self.call_remove_item(item.id)

        response = self.client.delete(reverse('item-detail', args=[item.id]))
        self.assertEqual(response.status_code, 404)


class RenameTests(APITestCase):
    def setUp(self):
        User.objects.create_user(**test_user)

    def call_rename(self, item_id, name):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[item_id]),
            data={'name': name}
        )
        self.assertEqual(response.status_code, 200)

    def test_rename_default(self):
        item = createItem('test')
        new_name = 'test2'

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_needed(self):
        item = createItem('test', needed=True)
        new_name = 'test2'

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertTrue(item.needed)
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_not_needed(self):
        item = createItem('test', needed=False)
        new_name = 'test2'

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertFalse(item.needed)
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_bought(self):
        item = createItem('test', bought=True)
        new_name = 'test2'

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertTrue(item.bought)
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_not_bought(self):
        item = createItem('test', bought=False)
        new_name = 'test2'

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertFalse(item.bought)
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_item_with_empty_name(self):
        item = createItem('')
        new_name = 'test2'

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_to_empty_name(self):
        item = createItem('test')
        new_name = ''

        self.call_rename(item.id, new_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_without_name_param(self):
        self.client.login(**test_user)
        name = 'test'
        item = createItem(name)

        response = self.client.patch(reverse('item-detail', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_not_logged_in(self):
        name = 'test'
        item = createItem(name)

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={'name': 'test2'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(item.name, name)

    def test_rename_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[0]),
            data={'name': 'test2'}
        )
        self.assertEqual(response.status_code, 404)


class ChangeCategoryTests(APITestCase):
    def setUp(self):
        self.new_category_name = 'test2'
        Category.objects.create(
            name=self.new_category_name,
            full_name='Test category 2'
        )
        User.objects.create_user(**test_user)

    def call_change_category(self, itemId, category):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[itemId]),
            data={'category': category}
        )
        self.assertEqual(response.status_code, 200)

    def test_change_category_default(self):
        name = 'test'
        item = createItem(name)

        self.call_change_category(item.id, self.new_category_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_needed(self):
        name = 'test'
        item = createItem(name, needed=True)

        self.call_change_category(item.id, self.new_category_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertTrue(item.needed)
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_not_needed(self):
        name = 'test'
        item = createItem(name, needed=False)

        self.call_change_category(item.id, self.new_category_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertFalse(item.needed)
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_bought(self):
        name = 'test'
        item = createItem(name, bought=True)

        self.call_change_category(item.id, self.new_category_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertTrue(item.bought)

    def test_change_category_not_bought(self):
        name = 'test'
        item = createItem(name, bought=False)

        self.call_change_category(item.id, self.new_category_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertFalse(item.bought)

    def test_change_category_item_with_empty_name(self):
        name = ''
        item = createItem(name)

        self.call_change_category(item.id, self.new_category_name)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_without_category_param(self):
        self.client.login(**test_user)
        item = createItem('test')
        old_category_name = item.category.name

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item.category.name, old_category_name)

    def test_change_category_not_logged_in(self):
        item = createItem('test')
        old_category_name = item.category.name

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(item.category.name, old_category_name)

    def test_change_category_not_existing_item(self):
        self.client.login(**test_user)
        response = self.client.patch(
            reverse('item-detail', args=[0]),
            data={'category': self.new_category_name}
        )
        self.assertEqual(response.status_code, 404)

    def test_change_category_not_existing_category(self):
        self.client.login(**test_user)
        item = createItem('test')
        old_category_name = item.category.name

        response = self.client.patch(
            reverse('item-detail', args=[item.id]),
            data={'category': 'lorem'}
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(item.category.name, old_category_name)

    def test_change_category_with_empty_category(self):
        self.client.login(**test_user)
        item = createItem('test')
        old_category_name = item.category.name

        self.call_change_category(item.id, '')
        self.assertEqual(item.category.name, old_category_name)
