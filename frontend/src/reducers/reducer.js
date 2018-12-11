import {
	REQUEST_ITEMS_SUCCEEDED,
	REQUEST_ITEMS_FAILED,
	TOGGLE_BOUGHT,
	TOGGLE_NEEDED,
	ADD_ITEM,
	REMOVE,
	RENAME,
	CHANGE_CATEGORY,
	MODE_SELECTED,
	TOGGLE_BOUGHT_FAILED,
	TOGGLE_NEEDED_FAILED,
	ADD_ITEM_FAILED,
	REMOVE_FAILED,
	RENAME_FAILED,
	CHANGE_CATEGORY_FAILED,
	NOW_OFFLINE,
	ADD_ITEM_OFFLINE,
	REQUEST_CATEGORIES_SUCCEEDED,
	REQUEST_CATEGORIES_FAILED,
} from '../actions/Actions';

const initialState = {
	items: [],
	loading: true,
	error: false,
	mode: 1,
	offline: false,
	categories: [],
};

const reducer = (state = initialState, action) => {
	switch (action.type) {
		case REQUEST_ITEMS_SUCCEEDED: {
			return Object.assign({}, state, {
				items: action.items,
				loading: false,
			});
		}
		case REQUEST_ITEMS_FAILED: {
			return {
				loading: false,
				error: true,
			};
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
		case CHANGE_CATEGORY: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.category = action.category;
					return item;
				}),
			});
		}
		case MODE_SELECTED: {
			return Object.assign({}, state, {
				mode: action.mode,
			});
		}
		case TOGGLE_BOUGHT_FAILED:
		case TOGGLE_NEEDED_FAILED:
		case ADD_ITEM_FAILED:
		case REMOVE_FAILED:
		case RENAME_FAILED:
		case CHANGE_CATEGORY_FAILED:
		case REQUEST_CATEGORIES_FAILED: {
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
			};
			return Object.assign({}, state, {
				items: state.items.concat(newItem),
				offline: true,
			});
		}
		case REQUEST_CATEGORIES_SUCCEEDED: {
			return Object.assign({}, state, {
				categories: action.categories,
			});
		}
		default:
			return state;
	}
};

export default reducer;
