import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

function getURIParams(params) {
	return Object.keys(params).reduce((prev, cur) => {
		return prev + (prev ? '&' : '') + `${cur}=${params[cur]}`;
	}, '');
}

class Api {
	static loadItems() {
		return axios.get('/ajax/items');
	}

	static loadCategories() {
		return axios.get('/ajax/categories');
	}

	static addItem(name, needed) {
		return axios.post('/ajax/add_item', getURIParams({ name: name, needed: needed }));
	}

	static toggleBought(id) {
		return axios.post('/ajax/toggle_bought', getURIParams({ item_id: id }));
	}

	static toggleNeeded(id) {
		return axios.post('/ajax/toggle_needed', getURIParams({ item_id: id }));
	}

	static remove(id) {
		return axios.post('/ajax/remove', getURIParams({ item_id: id }));
	}

	static rename(id, name) {
		return axios.post('/ajax/rename', getURIParams({ item_id: id, name: name }));
	}

	static changeCategory(id, category) {
		return axios.post(
			'/ajax/change_category',
			getURIParams({ item_id: id, category: category })
		);
	}
}

export default Api;
