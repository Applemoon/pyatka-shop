import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import TableComponent from '../components/TableComponent.jsx';
import Actions from '../actions/Actions';

class TableContainer extends PureComponent {
	getItems() {
		const { items, mode } = this.props;

		if (mode === 1) return items;

		return items
			.filter(el => el.needed)
			.sort((a, b) => (!a.bought && b.bought ? -1 : !b.bought && a.bought ? 1 : 0));
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
	loading: state.loading
});

const mapDispatchToProps = dispatch => ({
	loadItems: bindActionCreators(Actions.loadItems, dispatch),
	toggleStarred: bindActionCreators(Actions.toggleStarred, dispatch),
	toggleBought: bindActionCreators(Actions.toggleBought, dispatch),
	toggleNeeded: bindActionCreators(Actions.toggleNeeded, dispatch),
	remove: bindActionCreators(Actions.remove, dispatch),
	rename: bindActionCreators(Actions.rename, dispatch)
});

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(TableContainer);
