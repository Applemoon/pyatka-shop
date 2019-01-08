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
	static loadData() {
		return axios.get('/ajax/categories');
	}

	static addItem(name, category, needed) {
		return axios.post(
			'/ajax/items',
			getURIParams({ name: name, category: category, needed: needed })
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

	static edit(id, name, category, needed) {
		return axios.patch(
			`/ajax/items/${id}`,
			getURIParams({ name: name, category: category, needed: needed })
		);
	}

	static setAllNotBought() {
		return axios.patch('/ajax/items/all-not-bought');
	}
}

export default Api;
