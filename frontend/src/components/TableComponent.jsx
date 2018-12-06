import React from 'react';
import PropTypes from 'prop-types';
import { Table } from 'react-bootstrap';

import Item from './Item.jsx';

const TableComponent = ({
	items,
	mode,
	toggleBought,
	toggleNeeded,
	remove,
	rename,
	changeCategory,
	categories,
}) =>
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
						toggleBought={toggleBought}
						toggleNeeded={toggleNeeded}
						remove={remove}
						rename={rename}
						changeCategory={changeCategory}
						categories={categories}
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
			id: PropTypes.number.isRequired,
		}).isRequired
	).isRequired,
	mode: PropTypes.number.isRequired,
	toggleBought: PropTypes.func.isRequired,
	toggleNeeded: PropTypes.func.isRequired,
	remove: PropTypes.func.isRequired,
	rename: PropTypes.func.isRequired,
	changeCategory: PropTypes.func.isRequired,
	categories: PropTypes.arrayOf(
		PropTypes.shape({
			name: PropTypes.string.isRequired,
			full_name: PropTypes.string.isRequired,
		}).isRequired
	).isRequired,
};

export default TableComponent;
