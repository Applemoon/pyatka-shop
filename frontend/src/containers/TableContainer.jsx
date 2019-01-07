import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import TableComponent from '../components/TableComponent.jsx';
import Actions from '../actions/Actions';

class TableContainer extends PureComponent {
	sortByCategory = (itemA, itemB) => {
		return (
			this.props.categories.find(category => category.name === itemA.category).position -
			this.props.categories.find(category => category.name === itemB.category).position
		);
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
	setNeeded: bindActionCreators(Actions.setNeeded, dispatch),
	setNotNeeded: bindActionCreators(Actions.setNotNeeded, dispatch),
	setBought: bindActionCreators(Actions.setBought, dispatch),
	setNotBought: bindActionCreators(Actions.setNotBought, dispatch),
	remove: bindActionCreators(Actions.remove, dispatch),
	edit: bindActionCreators(Actions.edit, dispatch),
});

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(TableContainer);
