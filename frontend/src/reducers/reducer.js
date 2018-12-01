import {
	REQUESTED_ITEMS_SUCCEEDED,
	REQUESTED_ITEMS_FAILED,
	TOGGLE_STARRED,
	TOGGLE_BOUGHT,
	TOGGLE_NEEDED,
	ADD_ITEM,
	REMOVE,
	RENAME,
	MODE_SELECTED,
	TOGGLE_STARRED_FAILED,
	TOGGLE_BOUGHT_FAILED,
	TOGGLE_NEEDED_FAILED,
	ADD_ITEM_FAILED,
	REMOVE_FAILED,
	RENAME_FAILED,
	NOW_OFFLINE,
	ADD_ITEM_OFFLINE,
} from '../actions/Actions';

const initialState = {
	items: [],
	loading: true,
	error: false,
	mode: 1,
	offline: false,
};

const reducer = (state = initialState, action) => {
	switch (action.type) {
		case REQUESTED_ITEMS_SUCCEEDED: {
			return Object.assign({}, state, {
				items: action.items,
				loading: false,
			});
		}
		case REQUESTED_ITEMS_FAILED: {
			return {
				loading: false,
				error: true,
			};
		}
		case TOGGLE_STARRED: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.starred = !item.starred;
					return item;
				}),
			});
		}
		case TOGGLE_BOUGHT: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.bought = !item.bought;
					return item;
				}),
			});
		}
		case TOGGLE_NEEDED: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.needed = !item.needed;
					return item;
				}),
			});
		}
		case ADD_ITEM: {
			const newItem = {
				name: action.name,
				bought: action.bought,
				id: action.id,
				needed: action.needed,
				starred: action.starred,
				category: action.category,
			};
			return Object.assign({}, state, {
				items: state.items.concat(newItem),
			});
		}
		case REMOVE: {
			return Object.assign({}, state, {
				items: state.items.filter(item => {
					return item.id !== action.id;
				}),
			});
		}
		case RENAME: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.name = action.name;
					return item;
				}),
			});
		}
		case MODE_SELECTED: {
			return Object.assign({}, state, {
				mode: action.mode,
			});
		}
		case TOGGLE_STARRED_FAILED:
		case TOGGLE_BOUGHT_FAILED:
		case TOGGLE_NEEDED_FAILED:
		case ADD_ITEM_FAILED:
		case REMOVE_FAILED:
		case RENAME_FAILED: {
			return {
				error: true,
			};
		}
		case NOW_OFFLINE: {
			return Object.assign({}, state, {
				offline: true,
			});
		}
		case ADD_ITEM_OFFLINE: {
			const newItem = {
				name: action.name,
				bought: action.bought,
				id: -1,
				needed: action.needed,
				starred: action.starred,
			};
			return Object.assign({}, state, {
				items: state.items.concat(newItem),
				offline: true,
			});
		}
		default:
			return state;
	}
};

export default reducer;
