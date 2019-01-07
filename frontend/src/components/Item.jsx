import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Button, Glyphicon } from 'react-bootstrap';

import EditItemPopup from '../components/EditItemPopup.jsx';

class Item extends PureComponent {
	state = {
		editing: false,
		defaultName: this.props.name,
		defaultCategory: this.props.category,
		defaultNeeded: this.props.needed,
	};

	style = {
		verticalAlign: 'middle',
		whiteSpace: 'normal',
	};

	editStart = () => {
		this.setState({ editing: true });
	};

	handleEditingOk = (newName, newCategory, newNeeded) => {
		const { id, edit } = this.props;
		const { defaultName, defaultCategory, defaultNeeded } = this.state;

		const nameChanged = newName !== defaultName;
		const categoryChanged = newCategory !== defaultCategory;
		const neededChanged = newNeeded !== defaultNeeded;

		if (nameChanged || categoryChanged || neededChanged) {
			edit(id, newName, newCategory, newNeeded);
			this.setState({
				defaultName: newName,
				defaultCategory: newCategory,
				defaultNeeded: newNeeded,
			});
		}

		this.setState({ editing: false });
	};

	handleEditingCancel = () => {
		this.setState({ editing: false });
	};

	handleNameClick = () => {
		const {
			mode,
			id,
			needed,
			bought,
			setNeeded,
			setNotNeeded,
			setBought,
			setNotBought,
		} = this.props;
		mode === 1
			? !needed
				? setNeeded(id)
				: setNotNeeded(id)
			: !bought
			? setBought(id)
			: setNotBought(id);
	};

	render() {
		const {
			name,
			needed,
			bought,
			id,
			category,
			categories,
			mode,
			remove,
			setNotNeeded,
		} = this.props;
		const { style, editStart, handleEditingOk, handleEditingCancel, handleNameClick } = this;
		const editing = this.state.editing;

		const nameEl =
			needed && mode === 1 ? (
				<span>
					<Glyphicon glyph="shopping-cart" />
					<strong>{name}</strong>
					<Glyphicon glyph="shopping-cart" />
				</span>
			) : (
				name
			);

		return (
			<tr className={category + (mode === 2 && bought ? ' bought' : '')}>
				<td style={{ ...style }} onClick={handleNameClick}>
					{nameEl}
				</td>
				{mode === 1 ? (
					<td>
						<Button onClick={editStart}>✎</Button>
					</td>
				) : null}
				{mode === 1 ? (
					<td>
						<Button bsStyle="warning" onClick={() => remove(id)}>
							X
						</Button>
					</td>
				) : null}
				{mode === 2 ? (
					<td>
						<Button bsStyle="warning" onClick={() => setNotNeeded(id)}>
							-
						</Button>
					</td>
				) : null}

				<EditItemPopup
					name={name}
					category={category}
					needed={needed}
					show={editing}
					handleEditingOk={handleEditingOk}
					handleEditingCancel={handleEditingCancel}
					categories={categories}
				/>
			</tr>
		);
	}
}

Item.propTypes = {
	name: PropTypes.string.isRequired,
	bought: PropTypes.bool.isRequired,
	needed: PropTypes.bool.isRequired,
	id: PropTypes.number.isRequired,
	category: PropTypes.string.isRequired,
	mode: PropTypes.number.isRequired,
	setNeeded: PropTypes.func.isRequired,
	setNotNeeded: PropTypes.func.isRequired,
	setBought: PropTypes.func.isRequired,
	setNotBought: PropTypes.func.isRequired,
	remove: PropTypes.func.isRequired,
	edit: PropTypes.func.isRequired,
	categories: PropTypes.arrayOf(
		PropTypes.shape({
			name: PropTypes.string.isRequired,
			full_name: PropTypes.string.isRequired,
		}).isRequired
	).isRequired,
};

export default Item;
