import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Button, Form, FormGroup, InputGroup, FormControl, ControlLabel, Glyphicon } from 'react-bootstrap';

class Item extends PureComponent {
	state = {
		editing: false,
		name: this.props.name,
		defaultName: this.props.name,
	};

	editStart = () => {
		this.setState({ editing: true });
	};

	editDone = event => {
		event.preventDefault();
		if (this.state.name !== this.state.defaultName) {
			const { rename, id } = this.props;
			this.setState({ defaultName: this.state.name });
			rename(id, this.state.name);
		}
		this.setState({ editing: false });
	};

	handleChange = event => {
		this.setState({ name: event.target.value });
	};

	getCategoriesList = () => {
		const sortedCategories = this.props.categories.sort((a, b) => a.position - b.position);
		return sortedCategories.map((category, index) => (
			<option value={category.name} key={category.name}>
				{category.full_name}
			</option>
		));
	};

	onSelectChange = event => {
		this.props.changeCategory(this.props.id, this.input.value);
	};

	componentWillReceiveProps(nextProps) {
		if (nextProps.mode !== this.props.mode) {
			this.setState({ editing: false });
		}
	}

	render() {
		const { name, needed, bought, id, category, mode, toggleBought, toggleNeeded, remove } = this.props;
		const { editDone, handleChange, onSelectChange, editStart, getCategoriesList } = this;
		const editing = this.state.editing;

		return (
			<tr className={category + (mode === 2 && bought ? ' bought' : '')}>
				{!editing ? (
					<td
						style={{ verticalAlign: 'middle', paddingLeft: '20px' }}
						onClick={mode === 1 ? () => toggleNeeded(id) : () => toggleBought(id)}>
						{needed && mode === 1 ? (
							<span>
								<Glyphicon glyph="shopping-cart" />
								<strong>{name}</strong>
								<Glyphicon glyph="shopping-cart" />
							</span>
						) : (
							name
						)}
					</td>
				) : (
					<td style={{ verticalAlign: 'middle' }} colSpan="2">
						<Form inline onSubmit={editDone}>
							<FormGroup style={{ marginBottom: '0px' }}>
								<InputGroup>
									<FormControl
										type="text"
										defaultValue={name}
										placeholder={name}
										onChange={handleChange}
										autoFocus
									/>
									<InputGroup.Button>
										<Button type="submit" bsStyle="success">
											✓
										</Button>
									</InputGroup.Button>
								</InputGroup>
								<ControlLabel>Категория:</ControlLabel>
								<FormControl
									componentClass="select"
									placeholder={name}
									onChange={onSelectChange}
									inputRef={ref => (this.input = ref)}
									value={category}>
									{getCategoriesList()}
								</FormControl>
							</FormGroup>
						</Form>
					</td>
				)}
				{mode === 1 && !editing ? (
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

export default Item;
