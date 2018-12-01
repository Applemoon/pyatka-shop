import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

class Api {
	static loadItems() {
		return axios.get('/pyatka/ajax/items');
	}

	static addItem(name, needed) {
		return axios.post('/pyatka/ajax/add_item', {
			name: name,
			needed: needed,
		});
	}

	static toggleStarred(id) {
		return axios.post('/pyatka/ajax/toggle_starred', { item_id: id });
	}

	static toggleBought(id) {
		return axios.post('/pyatka/ajax/toggle_bought', { item_id: id });
	}

	static toggleNeeded(id) {
		return axios.post('/pyatka/ajax/toggle_needed', { item_id: id });
	}

	static remove(id) {
		return axios.post('/pyatka/ajax/remove', { item_id: id });
	}

	static rename(id, name) {
		return axios.post('/pyatka/ajax/rename', { item_id: id, name: name });
	}
}

export default Api;
