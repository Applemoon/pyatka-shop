import { createStore, applyMiddleware, compose } from 'redux';
import ReduxThunk from 'redux-thunk';
import reducer from './reducer.js';

// const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
// export const store = createStore(rootReducer, /* preloadedState, */ composeEnhancers(
// 	applyMiddleware(ReduxThunk)
// ));

export const store = createStore(reducer, applyMiddleware(ReduxThunk));
