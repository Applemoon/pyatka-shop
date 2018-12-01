import React from 'react';
import PropTypes from 'prop-types';
import { Table } from 'react-bootstrap';

import Item from './item.jsx';

const TableComponent = ({ items, mode, toggleStarred, toggleBought, toggleNeeded, remove, rename }) =>
	!items.length ? (
		<p>Список пуст</p>
	) : (
		<Table responsive>
			<tbody>
				{items.map(el => (
					<Item
						{...el}
						key={el.id}
						mode={mode}
						toggleStarred={toggleStarred}
						toggleBought={toggleBought}
						toggleNeeded={toggleNeeded}
						remove={remove}
						rename={rename}
					/>
				))}
			</tbody>
		</Table>
	);

TableComponent.propTypes = {
	items: PropTypes.arrayOf(
		PropTypes.shape({
			name: PropTypes.string.isRequired,
			bought: PropTypes.bool.isRequired,
			starred: PropTypes.bool.isRequired,
			id: PropTypes.number.isRequired,
		}).isRequired
	).isRequired,
	mode: PropTypes.number.isRequired,
	toggleStarred: PropTypes.func.isRequired,
	toggleBought: PropTypes.func.isRequired,
	toggleNeeded: PropTypes.func.isRequired,
	remove: PropTypes.func.isRequired,
	rename: PropTypes.func.isRequired,
};

export default TableComponent;
