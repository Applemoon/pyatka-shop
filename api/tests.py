from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from random import randrange
import json

from .models import Category, Item


default_item = {
    'needed': False,
    'bought': False,
    'category': 'other',
}


test_user = {
    'name': 'john',
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


class ItemsTests(TestCase):
    def setUp(self):
        Category.objects.create(
            name=default_item['category'],
            full_name='Test category'
        )
        User.objects.create_user(
            test_user['name'],
            test_user['email'],
            test_user['password']
        )

    def test_call_items_with_empty(self):
        self.client.login(
            username=test_user['name'],
            password=test_user['password']
        )

        response = self.client.get(reverse('items'))
        response_arr = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(response_arr), 0)

    def test_call_items_not_empty(self):
        self.client.login(
            username=test_user['name'],
            password=test_user['password']
        )
        [createItem(name) for name in 'test' + str(randrange(2, 20))]
        init_items_count = Item.objects.count()

        response = self.client.get(reverse('items'))
        response_arr = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(response_arr), Item.objects.count())
        self.assertEqual(len(response_arr), init_items_count)
        for resp_item in response_arr:
            item = Item.objects.get(pk=resp_item['id'])
            self.assertEqual(item.name, resp_item['name'])
            self.assertEqual(item.needed, resp_item['needed'])
            self.assertEqual(item.bought, resp_item['bought'])

    def test_call_items_not_logged_in(self):
        response = self.client.get(reverse('items'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/ajax/items')

    def test_call_items_post_method(self):
        self.client.login(
            username=test_user['name'],
            password=test_user['password']
        )

        response = self.client.post(reverse('items'))
        self.assertEqual(response.status_code, 405)


class CategoriesTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            test_user['name'],
            test_user['email'],
            test_user['password']
        )

    def test_call_categories_with_empty(self):
        self.client.login(
            username=test_user['name'],
            password=test_user['password']
        )

        response = self.client.get(reverse('categories'))
        response_arr = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(response_arr), 0)

    def test_call_categories_not_empty(self):
        self.client.login(
            username=test_user['name'],
            password=test_user['password']
        )
        [Category.objects.create(
            name='test' + str(i), full_name='Test category ' + str(i))
            for i in range(2, randrange(3, 20))]
        init_categories_count = Category.objects.count()

        response = self.client.get(reverse('categories'))
        response_arr = json.loads(response.content.decode("utf-8"))
        self.assertEqual(len(response_arr), Category.objects.count())
        self.assertEqual(len(response_arr), init_categories_count)

    def test_call_categories_not_logged_in(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/ajax/categories')

    def test_call_categories_post_method(self):
        self.client.login(
            username=test_user['name'],
            password=test_user['password']
        )

        response = self.client.post(reverse('categories'))
        self.assertEqual(response.status_code, 405)


class AddItemTests(TestCase):
    def setUp(self):
        Category.objects.create(
            name=default_item['category'],
            full_name='Test category'
        )

    def call_add_item(self, data):
        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_create_default_item(self):
        name = 'test'
        data = {'name': name}
        init_items_count = Item.objects.count()

        response_dict = self.call_add_item(data)
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

        response_dict = self.call_add_item(data)
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

        response_dict = self.call_add_item(data)
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

        response_dict = self.call_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertFalse(response_dict['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], category_2.name)
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_needed_item(self):
        name = 'test'
        data = {'name': name, 'needed': 'true'}
        init_items_count = Item.objects.count()

        response_dict = self.call_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], True)
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], default_item['category'])
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_not_needed_item(self):
        name = 'test'
        data = {'name': name, 'needed': 'false'}
        init_items_count = Item.objects.count()

        response_dict = self.call_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], False)
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertEqual(response_dict['category'], default_item['category'])
        self.assertTrue('id' in response_dict)
        self.assertEqual(Item.objects.count(), init_items_count + 1)

    def test_create_item_with_empty_data(self):
        data = {}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_create_item_with_no_name(self):
        data = {'needed': 'true', 'category': default_item['category']}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_create_item_with_wrong_needed(self):
        data = {'name': 'test', 'needed': 'test2'}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_create_item_with_long_name(self):
        name = 'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23'
        data = {'name': name}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_create_with_wrond_category(self):
        data = {'name': 'test', 'category': 'wrong'}
        init_items_count = Item.objects.count()

        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Item.objects.count(), init_items_count)

    def test_add_item_get_method(self):
        name = 'test'
        data = {'name': name}
        init_items_count = Item.objects.count()

        response = self.client.get(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Item.objects.count(), init_items_count)


class SetNeededTests(TestCase):
    def call_set_needed(self, data):
        response = self.client.post(reverse('set_needed'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_set_needed_default(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response_dict = self.call_set_needed(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertTrue(item.needed)

    def test_set_needed_needless(self):
        item = createItem('test', needed=False)
        data = {'item_id': item.id}

        response_dict = self.call_set_needed(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertTrue(item.needed)

    def test_set_needed_needed(self):
        item = createItem('test', needed=True)
        data = {'item_id': item.id}

        response_dict = self.call_set_needed(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertTrue(item.needed)

    def test_set_needed_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('set_needed'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_set_needed_not_existing_item(self):
        data = {'item_id': -1}

        response = self.client.post(reverse('set_needed'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_set_needed_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.get(reverse('set_needed'), data=data)
        self.assertEqual(response.status_code, 405)


class SetNotNeededTests(TestCase):
    def call_set_not_needed(self, data):
        response = self.client.post(reverse('set_not_needed'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_set_not_needed_default(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response_dict = self.call_set_not_needed(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertFalse(item.needed)

    def test_set_not_needed_needless(self):
        item = createItem('test', needed=False)
        data = {'item_id': item.id}

        response_dict = self.call_set_not_needed(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertFalse(item.needed)

    def test_set_not_needed_needed(self):
        item = createItem('test', needed=True)
        data = {'item_id': item.id}

        response_dict = self.call_set_not_needed(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertFalse(item.needed)

    def test_set_not_needed_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('set_not_needed'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_set_not_needed_not_existing_item(self):
        data = {'item_id': -1}

        response = self.client.post(reverse('set_not_needed'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_set_not_needed_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.get(reverse('set_not_needed'), data=data)
        self.assertEqual(response.status_code, 405)


class SetBoughtTests(TestCase):
    def call_set_bought(self, data):
        response = self.client.post(reverse('set_bought'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_set_bought_default(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response_dict = self.call_set_bought(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertTrue(item.bought)

    def test_set_bought_not_bought(self):
        item = createItem('test', bought=False)
        data = {'item_id': item.id}

        response_dict = self.call_set_bought(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertTrue(item.bought)

    def test_set_bought_bought(self):
        item = createItem('test', bought=True)
        data = {'item_id': item.id}

        response_dict = self.call_set_bought(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertTrue(item.bought)

    def test_set_bought_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('set_bought'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_set_bought_not_existing_item(self):
        data = {'item_id': -1}

        response = self.client.post(reverse('set_bought'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_set_bought_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.get(reverse('set_bought'), data=data)
        self.assertEqual(response.status_code, 405)


class SetNotBoughtTests(TestCase):
    def call_set_not_bought(self, data):
        response = self.client.post(reverse('set_not_bought'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_set_not_bought_default(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response_dict = self.call_set_not_bought(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertFalse(item.bought)

    def test_set_not_bought_not_bought(self):
        item = createItem('test', bought=False)
        data = {'item_id': item.id}

        response_dict = self.call_set_not_bought(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertFalse(item.bought)

    def test_set_not_bought_bought(self):
        item = createItem('test', bought=True)
        data = {'item_id': item.id}

        response_dict = self.call_set_not_bought(data)
        self.assertEqual(response_dict['status'], 'ok')
        item = Item.objects.get(pk=item.id)
        self.assertFalse(item.bought)

    def test_set_not_bought_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('set_not_bought'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_set_not_bought_not_existing_item(self):
        data = {'item_id': -1}

        response = self.client.post(reverse('set_not_bought'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_set_not_bought_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.get(reverse('set_not_bought'), data=data)
        self.assertEqual(response.status_code, 405)


class RemoveTests(TestCase):
    def call_remove_item(self, data):
        response = self.client.post(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_dict['status'], 'ok')
        return response

    def test_remove_default_item(self):
        item = createItem('test')
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_last_item(self):
        item = createItem('test1')
        createItem('test2')
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 1)
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=item.id)

    def test_remove_needed_item(self):
        item = createItem('test', needed=True)
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_needed_item(self):
        item = createItem('test', needed=False)
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_bought_item(self):
        item = createItem('test', bought=True)
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_not_bought_item(self):
        item = createItem('test', bought=False)
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_item_with_empty_name(self):
        item = createItem('')
        data = {'item_id': item.id}

        self.call_remove_item(data)
        self.assertEqual(Item.objects.count(), 0)

    def test_remove_item_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_remove_not_existing_item(self):
        data = {'item_id': -1}

        response = self.client.post(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_double_remove(self):
        item = createItem('test')
        data = {'item_id': item.id}
        self.call_remove_item(data)

        response = self.client.post(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_remove_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.get(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 405)


class RenameTests(TestCase):
    def call_rename(self, data):
        response = self.client.post(reverse('rename'), data=data)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_dict['status'], 'ok')
        return response

    def test_rename_default(self):
        item = createItem('test')
        new_name = 'test2'
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_needed(self):
        item = createItem('test', needed=True)
        new_name = 'test2'
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertTrue(item.needed)
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_not_needed(self):
        item = createItem('test', needed=False)
        new_name = 'test2'
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertFalse(item.needed)
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_bought(self):
        item = createItem('test', bought=True)
        new_name = 'test2'
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertTrue(item.bought)
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_not_bought(self):
        item = createItem('test', bought=False)
        new_name = 'test2'
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertFalse(item.bought)
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_item_with_empty_name(self):
        item = createItem('')
        new_name = 'test2'
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_to_empty_name(self):
        item = createItem('test')
        new_name = ''
        data = {'item_id': item.id, 'name': new_name}

        self.call_rename(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.name, new_name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])
        self.assertEqual(item.category.name, default_item['category'])

    def test_rename_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('rename'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_rename_without_name_param(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.post(reverse('rename'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_rename_without_id_param(self):
        data = {'name': 'test2'}

        response = self.client.post(reverse('rename'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_rename_not_existing_item(self):
        data = {'item_id': -1, 'name': 'test2'}

        response = self.client.post(reverse('rename'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_rename_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id, 'name': 'test2'}

        response = self.client.get(reverse('rename'), data=data)
        self.assertEqual(response.status_code, 405)


class ChangeCategoryTests(TestCase):
    def setUp(self):
        self.new_category_name = 'test2'
        Category.objects.create(
            name=self.new_category_name,
            full_name='Test category 2'
        )

    def call_change_category(self, data):
        response = self.client.post(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_dict['status'], 'ok')
        return response

    def test_change_category_default(self):
        name = 'test'
        item = createItem(name)
        data = {'item_id': item.id, 'category': self.new_category_name}

        self.call_change_category(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_needed(self):
        name = 'test'
        item = createItem(name, needed=True)
        data = {'item_id': item.id, 'category': self.new_category_name}

        self.call_change_category(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertTrue(item.needed)
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_not_needed(self):
        name = 'test'
        item = createItem(name, needed=False)
        data = {'item_id': item.id, 'category': self.new_category_name}

        self.call_change_category(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertFalse(item.needed)
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_bought(self):
        name = 'test'
        item = createItem(name, bought=True)
        data = {'item_id': item.id, 'category': self.new_category_name}

        self.call_change_category(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertTrue(item.bought)

    def test_change_category_not_bought(self):
        name = 'test'
        item = createItem(name, bought=False)
        data = {'item_id': item.id, 'category': self.new_category_name}

        self.call_change_category(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertFalse(item.bought)

    def test_change_category_item_with_empty_name(self):
        name = ''
        item = createItem(name)
        data = {'item_id': item.id, 'category': self.new_category_name}

        self.call_change_category(data)
        item = Item.objects.get(pk=item.id)
        self.assertEqual(item.category.name, self.new_category_name)
        self.assertEqual(item.name, name)
        self.assertEqual(item.needed, default_item['needed'])
        self.assertEqual(item.bought, default_item['bought'])

    def test_change_category_with_empty_data(self):
        data = {}

        response = self.client.post(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_change_category_without_category_param(self):
        item = createItem('test')
        data = {'item_id': item.id}

        response = self.client.post(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_change_category_without_id_param(self):
        data = {'category': self.new_category_name}

        response = self.client.post(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_change_category_not_existing_item(self):
        data = {'item_id': -1, 'category': self.new_category_name}

        response = self.client.post(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_change_category_not_existing_category(self):
        item = createItem('test')
        data = {'item_id': item.id, 'category': 'lorem'}

        response = self.client.post(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_change_category_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id, 'category': self.new_category_name}

        response = self.client.get(reverse('change_category'), data=data)
        self.assertEqual(response.status_code, 405)
