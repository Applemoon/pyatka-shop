import Api from './Api';

export const REQUESTED_ITEMS_SUCCEEDED = 'REQUESTED_ITEMS_SUCCEEDED';
export const REQUESTED_ITEMS_FAILED = 'REQUESTED_ITEMS_FAILED';

export const TOGGLE_STARRED = 'TOGGLE_STARRED';
export const TOGGLE_STARRED_FAILED = 'TOGGLE_STARRED_FAILED';

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

export const MODE_SELECTED = 'MODE_SELECTED';

export const NOW_OFFLINE = 'NOW_OFFLINE';
export const ADD_ITEM_OFFLINE = 'ADD_ITEM_OFFLINE';

export const EDIT_ITEM = 'EDIT_ITEM';

const DEFAULT_ITEM = {
	id: -1,
	needed: false,
	bought: false,
	starred: false,
	category: 'other',
};

class Actions {
	static loadItems = () => dispatch => {
		Api.loadItems()
			.then(function(result) {
				return dispatch({
					type: REQUESTED_ITEMS_SUCCEEDED,
					items: result.data,
				});
			})
			.catch(err => {
				dispatch({ type: REQUESTED_ITEMS_FAILED });
			});
	};

	static toggleStarred = id => dispatch => {
		dispatch({
			type: TOGGLE_STARRED,
			id: id,
		});

		Api.toggleStarred(id).catch(err => {
			!err.response ? dispatch({ type: NOW_OFFLINE }) : dispatch({ type: TOGGLE_STARRED_FAILED });
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
					starred: result.data.starred,
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
							starred: DEFAULT_ITEM.starred,
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

	static selectMode = mode => dispatch => {
		dispatch({
			type: MODE_SELECTED,
			mode: mode,
		});
	};

	static editItem = id => dispatch => {
		dispatch({
			type: EDIT_ITEM,
			id: id,
		});
	};
}

export default Actions;
