import {
	REQUEST_ITEMS_SUCCEEDED,
	SET_NEEDED,
	SET_NOT_NEEDED,
	SET_BOUGHT,
	SET_NOT_BOUGHT,
	ADD_ITEM,
	REMOVE,
	RENAME,
	CHANGE_CATEGORY,
	MODE_1_SELECTED,
	MODE_2_SELECTED,
	NOW_OFFLINE,
	ADD_ITEM_OFFLINE,
	REQUEST_CATEGORIES_SUCCEEDED,
	REQUEST_FAILED,
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
		case SET_NEEDED: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.needed = true;
					return item;
				}),
			});
		}
		case SET_NOT_NEEDED: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.needed = false;
					return item;
				}),
			});
		}
		case SET_BOUGHT: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.bought = true;
					return item;
				}),
			});
		}
		case SET_NOT_BOUGHT: {
			return Object.assign({}, state, {
				items: state.items.map(item => {
					if (item.id == action.id) item.bought = false;
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
		case MODE_1_SELECTED: {
			return Object.assign({}, state, {
				mode: 1,
				items: state.items.map(item => {
					item.bought = false;
					return item;
				}),
			});
		}
		case MODE_2_SELECTED: {
			return Object.assign({}, state, {
				mode: 2,
			});
		}
		case REQUEST_FAILED: {
			return {
				loading: false,
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
			const sortedCategories = action.categories.sort((a, b) => a.position - b.position);
			return Object.assign({}, state, {
				categories: sortedCategories,
			});
		}
		default:
			return state;
	}
};

export default reducer;
