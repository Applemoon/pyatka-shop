from django.test import TestCase
from django.urls import reverse
import json

from .models import Category, Item


default_item = {
    'needed': False,
    'bought': False
}


def getCategory():
    if Category.objects.count() == 0:
        return Category.objects.create(
            name='test',
            full_name='This is a test category'
        )

    return Category.objects.first()


def createItem(name, needed=default_item['needed']):
    return Item.objects.create(
        name=name,
        needed=needed,
        category=getCategory()
    )


class AddItemTests(TestCase):
    def setUp(self):
        Category.objects.create(name='test', full_name='Test category')

    def call_add_item(self, data):
        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_create_default_item(self):
        name = 'test'
        data = {'name': name}
        response_dict = self.call_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], default_item['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertTrue('id' in response_dict)

    def test_create_needed_item(self):
        name = 'test'
        data = {'name': name, 'needed': 'true'}
        response_dict = self.call_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['needed'], not default_item['needed'])
        self.assertEqual(response_dict['bought'], default_item['bought'])
        self.assertTrue('id' in response_dict)

    def test_create_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_item_with_wrong_needed(self):
        data = {'name': 'test', 'needed': 'test2'}
        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_item_with_long_name(self):
        name = 'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23'
        data = {'name': name}
        response = self.client.post(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_add_item_get_method(self):
        name = 'test'
        data = {'name': name}
        response = self.client.get(reverse('add_item'), data=data)
        self.assertEqual(response.status_code, 405)


class ToggleNeededItemTests(TestCase):
    def call_toggle_needed_item(self, data):
        response = self.client.post(reverse('toggle_needed'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_toggle_needed_default_item(self):
        name = 'test'
        item = createItem(name)
        data = {'item_id': item.id}
        response_dict = self.call_toggle_needed_item(data)
        self.assertEqual(response_dict['status'], 'ok')

    def test_needed_item(self):
        name = 'test'
        item = createItem(name, needed=False)
        data = {'item_id': item.id}
        response_dict = self.call_toggle_needed_item(data)
        self.assertEqual(response_dict['status'], 'ok')

    def test_toggle_needed_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('toggle_needed'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_toggle_needed_not_existing_item(self):
        data = {'item_id': -1}
        response = self.client.post(reverse('toggle_needed'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_toggle_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}
        response = self.client.get(reverse('toggle_needed'), data=data)
        self.assertEqual(response.status_code, 405)


class RemoveItemTests(TestCase):
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

    def test_remove_needed_item(self):
        item = createItem('test', needed=(not default_item['needed']))
        data = {'item_id': item.id}
        self.call_remove_item(data)

    def test_remove_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_remove_not_existing_item(self):
        data = {'item_id': -1}
        response = self.client.post(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_remove_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}
        response = self.client.get(reverse('remove'), data=data)
        self.assertEqual(response.status_code, 405)
