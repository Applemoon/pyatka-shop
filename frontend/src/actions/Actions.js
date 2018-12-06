import Api from './Api';

export const REQUEST_ITEMS_SUCCEEDED = 'REQUEST_ITEMS_SUCCEEDED';
export const REQUEST_ITEMS_FAILED = 'REQUEST_ITEMS_FAILED';

export const TOGGLE_BOUGHT = 'TOGGLE_BOUGHT';
export const TOGGLE_BOUGHT_FAILED = 'TOGGLE_BOUGHT_FAILED';

export const TOGGLE_NEEDED = 'TOGGLE_NEEDED';
export const TOGGLE_NEEDED_FAILED = 'TOGGLE_NEEDED_FAILED';

export const ADD_ITEM = 'ADD_ITEM';
export const ADD_ITEM_FAILED = 'ADD_ITEM_FAILED';

export const REMOVE = 'REMOVE';
export const REMOVE_FAILED = 'REMOVE_FAILED';

export const RENAME = 'RENAME';
export const RENAME_FAILED = 'RENAME_FAILED';

export const CHANGE_CATEGORY = 'CHANGE_CATEGORY';
export const CHANGE_CATEGORY_FAILED = 'CHANGE_CATEGORY_FAILED';

export const MODE_SELECTED = 'MODE_SELECTED';

export const NOW_OFFLINE = 'NOW_OFFLINE';
export const ADD_ITEM_OFFLINE = 'ADD_ITEM_OFFLINE';

export const EDIT_ITEM = 'EDIT_ITEM';

export const REQUEST_CATEGORIES_SUCCEEDED = 'REQUEST_CATEGORIES_SUCCEEDED';
export const REQUEST_CATEGORIES_FAILED = 'REQUEST_CATEGORIES_FAILED';

const DEFAULT_ITEM = {
	id: -1,
	needed: false,
	bought: false,
	category: 'other',
};

class Actions {
	static loadItems = () => dispatch => {
		Api.loadItems()
			.then(function(result) {
				return dispatch({
					type: REQUEST_ITEMS_SUCCEEDED,
					items: result.data,
				});
			})
			.catch(err => {
				dispatch({ type: REQUEST_ITEMS_FAILED });
			});
	};

	static toggleBought = id => dispatch => {
		dispatch({
			type: TOGGLE_BOUGHT,
			id: id,
		});

		Api.toggleBought(id).catch(err => {
			!err.response ? dispatch({ type: NOW_OFFLINE }) : dispatch({ type: TOGGLE_BOUGHT_FAILED });
		});
	};

	static toggleNeeded = id => dispatch => {
		dispatch({
			type: TOGGLE_NEEDED,
			id: id,
		});

		Api.toggleNeeded(id).catch(err => {
			!err.response ? dispatch({ type: NOW_OFFLINE }) : dispatch({ type: TOGGLE_NEEDED_FAILED });
		});
	};

	static addItem = (name, needed = DEFAULT_ITEM.needed) => dispatch => {
		Api.addItem(name, needed)
			.then(result => {
				dispatch({
					type: ADD_ITEM,
					name: name,
					bought: result.data.bought,
					id: result.data.id,
					needed: needed,
					category: DEFAULT_ITEM.category,
				});
			})
			.catch(err => {
				!err.response
					? dispatch({
							type: ADD_ITEM_OFFLINE,
							name: name,
							bought: DEFAULT_ITEM.bought,
							needed: needed,
							category: DEFAULT_ITEM.category,
					  })
					: dispatch({ type: ADD_ITEM_FAILED });
			});
	};

	static remove = id => dispatch => {
		dispatch({
			type: REMOVE,
			id: id,
		});

		Api.remove(id).catch(err => {
			!err.response ? dispatch({ type: NOW_OFFLINE }) : dispatch({ type: REMOVE_FAILED });
		});
	};

	static rename = (id, name) => dispatch => {
		dispatch({
			type: RENAME,
			id: id,
			name: name,
		});

		Api.rename(id, name).catch(err => {
			!err.response ? dispatch({ type: NOW_OFFLINE }) : dispatch({ type: RENAME_FAILED });
		});
	};

	static changeCategory = (id, category) => dispatch => {
		dispatch({
			type: CHANGE_CATEGORY,
			id: id,
			category: category,
		});

		Api.changeCategory(id, category).catch(err => {
			!err.response ? dispatch({ type: NOW_OFFLINE }) : dispatch({ type: CHANGE_CATEGORY_FAILED });
		});
	};

	static selectMode = mode => dispatch => {
		dispatch({
			type: MODE_SELECTED,
			mode: mode,
		});
	};

	static loadCategories = () => dispatch => {
		Api.loadCategories()
			.then(function(result) {
				return dispatch({
					type: REQUEST_CATEGORIES_SUCCEEDED,
					categories: result.data,
				});
			})
			.catch(err => {
				dispatch({ type: REQUEST_CATEGORIES_FAILED });
			});
	};
}

export default Actions;
