from django.test import TestCase
from django.urls import reverse
import json

from .models import Item


def createItem(name, needed=True, starred=False):
    return Item.objects.create(name=name, needed=needed, starred=starred)


class IndexTests(TestCase):
    def test_unreg_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        # TODO check response

    def test_index_post_method(self):
        response = self.client.post(reverse('index'))
        self.assertEqual(response.status_code, 405)


class AddItemTests(TestCase):
    def call_ajax_add_item(self, data):
        response = self.client.post(reverse('ajax_add_item'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_create_default_item(self):
        name = 'test'
        data = {'name': name}
        response_dict = self.call_ajax_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], False)
        self.assertEqual(response_dict['needed'], True)
        self.assertTrue('id' in response_dict)

    def test_create_unckecked_item(self):
        name = 'test'
        data = {'name': name, 'needed': 'false'}
        response_dict = self.call_ajax_add_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], False)
        self.assertEqual(response_dict['needed'], False)
        self.assertTrue('id' in response_dict)

    def test_create_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('ajax_add_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_item_with_wrong_needed(self):
        data = {'name': 'test', 'needed': 'test2'}
        response = self.client.post(reverse('ajax_add_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_item_with_long_name(self):
        name = 'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23' +\
            'dkfjo2u3ron23rn2lk3nlk2j34lk2j34lkj234lkj234lkn23'
        data = {'name': name}
        response = self.client.post(reverse('ajax_add_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_add_item_get_method(self):
        name = 'test'
        data = {'name': name}
        response = self.client.get(reverse('ajax_add_item'), data=data)
        self.assertEqual(response.status_code, 405)


class ToggleItemTests(TestCase):
    def call_ajax_toggle_item(self, data):
        response = self.client.post(reverse('ajax_toggle_item'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_toggle_default_item(self):
        name = 'test'
        item = createItem(name)
        data = {'item_id': item.id}
        response_dict = self.call_ajax_toggle_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], False)
        self.assertEqual(response_dict['needed'], False)
        self.assertEqual(response_dict['id'], item.id)

    def test_ckeck_item(self):
        name = 'test'
        item = createItem(name, needed=False)
        data = {'item_id': item.id}
        response_dict = self.call_ajax_toggle_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], False)
        self.assertEqual(response_dict['needed'], True)
        self.assertEqual(response_dict['id'], item.id)

    def test_toggle_starred_item(self):
        name = 'test'
        item = createItem(name, starred=True)
        data = {'item_id': item.id}
        response_dict = self.call_ajax_toggle_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], True)
        self.assertEqual(response_dict['needed'], False)
        self.assertEqual(response_dict['id'], item.id)

    def test_toggle_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('ajax_toggle_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_toggle_not_existing_item(self):
        data = {'item_id': -1}
        response = self.client.post(reverse('ajax_toggle_item'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_toggle_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}
        response = self.client.get(reverse('ajax_toggle_item'), data=data)
        self.assertEqual(response.status_code, 405)


class StarItemTests(TestCase):
    def call_ajax_star_item(self, data):
        response = self.client.post(reverse('ajax_star_item'), data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def test_star_default_item(self):
        name = 'test'
        item = createItem(name)
        data = {'item_id': item.id}
        response_dict = self.call_ajax_star_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], True)
        self.assertEqual(response_dict['needed'], True)
        self.assertEqual(response_dict['id'], item.id)

    def test_unstar_item(self):
        name = 'test'
        item = createItem(name, starred=True)
        data = {'item_id': item.id}
        response_dict = self.call_ajax_star_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], False)
        self.assertEqual(response_dict['needed'], True)
        self.assertEqual(response_dict['id'], item.id)

    def test_star_needless_item(self):
        name = 'test'
        item = createItem(name, needed=False)
        data = {'item_id': item.id}
        response_dict = self.call_ajax_star_item(data)
        self.assertEqual(response_dict['name'], name)
        self.assertEqual(response_dict['starred'], True)
        self.assertEqual(response_dict['needed'], False)
        self.assertEqual(response_dict['id'], item.id)

    def test_star_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('ajax_star_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_star_not_existing_item(self):
        data = {'item_id': -1}
        response = self.client.post(reverse('ajax_star_item'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_star_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}
        response = self.client.get(reverse('ajax_star_item'), data=data)
        self.assertEqual(response.status_code, 405)


class RemoveItemTests(TestCase):
    def call_ajax_remove_item(self, data):
        response = self.client.post(reverse('ajax_remove_item'), data=data)
        self.assertEqual(response.status_code, 200)

        response_dict = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_dict['status'], 'ok')
        return response

    def test_remove_default_item(self):
        item = createItem('test')
        data = {'item_id': item.id}
        self.call_ajax_remove_item(data)

    def test_remove_starred_item(self):
        item = createItem('test', starred=True)
        data = {'item_id': item.id}
        self.call_ajax_remove_item(data)

    def test_remove_needless_item(self):
        item = createItem('test', needed=False)
        data = {'item_id': item.id}
        self.call_ajax_remove_item(data)

    def test_remove_item_with_empty_data(self):
        data = {}
        response = self.client.post(reverse('ajax_remove_item'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_remove_not_existing_item(self):
        data = {'item_id': -1}
        response = self.client.post(reverse('ajax_remove_item'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_remove_item_get_method(self):
        item = createItem('test')
        data = {'item_id': item.id}
        response = self.client.get(reverse('ajax_remove_item'), data=data)
        self.assertEqual(response.status_code, 405)
