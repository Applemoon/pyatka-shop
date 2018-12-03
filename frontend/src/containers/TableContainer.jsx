import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import TableComponent from '../components/TableComponent.jsx';
import Actions from '../actions/Actions';

class TableContainer extends PureComponent {
	sortByCategory = (a, b) => {
		return a.category > b.category ? 1 : a.category === b.category ? 0 : -1;
	};

	getItems() {
		const { items, mode } = this.props;

		if (mode === 1) return items.sort(this.sortByCategory);

		const notBought = items.filter(el => el.needed && !el.bought).sort(this.sortByCategory);
		const bought = items.filter(el => el.needed && el.bought).sort(this.sortByCategory);
		return notBought.concat(bought);
	}

	render() {
		return <TableComponent {...this.props} items={this.getItems()} />;
	}
}

const mapStateToProps = state => ({
	items: state.items,
	error: state.error,
	mode: state.mode,
	offline: state.offline,
	loading: state.loading,
	categories: state.categories,
});

const mapDispatchToProps = dispatch => ({
	loadItems: bindActionCreators(Actions.loadItems, dispatch),
	toggleStarred: bindActionCreators(Actions.toggleStarred, dispatch),
	toggleBought: bindActionCreators(Actions.toggleBought, dispatch),
	toggleNeeded: bindActionCreators(Actions.toggleNeeded, dispatch),
	remove: bindActionCreators(Actions.remove, dispatch),
	rename: bindActionCreators(Actions.rename, dispatch),
	changeCategory: bindActionCreators(Actions.changeCategory, dispatch),
});

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(TableContainer);
