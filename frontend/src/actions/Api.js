import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.post['Content-Type'] =
	'application/x-www-form-urlencoded';

function getURIParams(params) {
	return Object.keys(params).reduce((prev, cur) => {
		return prev + (prev ? '&' : '') + `${cur}=${params[cur]}`;
	}, '');
}

class Api {
	static loadItems() {
		return axios.get('/pyatka/ajax/items');
	}

	static loadCategories() {
		return axios.get('/pyatka/ajax/categories');
	}

	static addItem(name, needed) {
		return axios.post(
			'/pyatka/ajax/add_item',
			getURIParams({ name: name, needed: needed })
		);
	}

	static toggleBought(id) {
		return axios.post(
			'/pyatka/ajax/toggle_bought',
			getURIParams({ item_id: id })
		);
	}

	static toggleNeeded(id) {
		return axios.post(
			'/pyatka/ajax/toggle_needed',
			getURIParams({ item_id: id })
		);
	}

	static remove(id) {
		return axios.post('/pyatka/ajax/remove', getURIParams({ item_id: id }));
	}

	static rename(id, name) {
		return axios.post(
			'/pyatka/ajax/rename',
			getURIParams({ item_id: id, name: name })
		);
	}

	static changeCategory(id, category) {
		return axios.post(
			'/pyatka/ajax/change_category',
			getURIParams({ item_id: id, category: category })
		);
	}
}

export default Api;
