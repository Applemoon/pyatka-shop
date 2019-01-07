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

	static addItem(name, needed, category) {
		return axios.post(
			'/ajax/items',
			getURIParams({ name: name, needed: needed, category: category })
		);
	}

	static setNeeded(id) {
		return axios.patch(`/ajax/items/${id}`, getURIParams({ needed: true }));
	}

	static setNotNeeded(id) {
		return axios.patch(`/ajax/items/${id}`, getURIParams({ needed: false }));
	}

	static setBought(id) {
		return axios.patch(`/ajax/items/${id}`, getURIParams({ bought: true }));
	}

	static setNotBought(id) {
		return axios.patch(`/ajax/items/${id}`, getURIParams({ bought: false }));
	}

	static remove(id) {
		return axios.delete('/ajax/items/' + id);
	}

	static rename(id, name) {
		return axios.patch(`/ajax/items/${id}`, getURIParams({ name: name }));
	}

	static changeCategory(id, category) {
		return axios.patch(`/ajax/items/${id}`, getURIParams({ category: category }));
	}

	static setAllNotBought() {
		return axios.post('/ajax/all_not_bought');
	}
}

export default Api;
