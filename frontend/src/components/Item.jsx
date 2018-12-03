import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Button, Form, FormGroup, InputGroup, FormControl, ControlLabel, Glyphicon } from 'react-bootstrap';

class Item extends PureComponent {
	state = {
		editing: false,
		name: this.props.name,
	};

	editStart = () => {
		this.setState({ editing: true });
	};

	editDone = event => {
		event.preventDefault();
		const { rename, id } = this.props;
		rename(id, this.state.name);
		this.setState({ editing: false });
	};

	handleChange = event => {
		this.setState({ name: event.target.value });
	};

	translateCategory = () => {
		const { categories, category } = this.props;
		const translate = categories.find(el => el.key === category);
		if (translate) return translate.value;
		return category;
	};

	getCategoriesList = () => {
		const index = this.props.categories.findIndex(el => el.key === this.props.category);
		const newCategory = {
			key: this.props.category,
			value: this.translateCategory(this.props.category),
		};
		const sortedCategories = [newCategory]
			.concat(this.props.categories.slice(0, index))
			.concat(this.props.categories.slice(index + 1, this.props.categories.length));

		return sortedCategories.map((category, index) => (
			<option value={category.key} key={category.key}>
				{category.value}
			</option>
		));
	};

	onSelectChange = event => {
		const { changeCategory, id } = this.props;
		changeCategory(id, this.input.value);
	};

	render() {
		const {
			name,
			starred,
			needed,
			bought,
			id,
			category,
			mode,
			toggleStarred,
			toggleBought,
			toggleNeeded,
			remove,
		} = this.props;

		return (
			<tr className={category + (mode === 2 && bought ? ' bought' : '')}>
				{!this.state.editing ? (
					<td
						style={{ verticalAlign: 'middle', paddingLeft: '20px' }}
						onClick={mode === 1 ? () => toggleNeeded(id) : () => toggleBought(id)}>
						{needed && mode === 1 ? (
							<span>
								<Glyphicon glyph="shopping-cart" /> <strong>{name}</strong>{' '}
								<Glyphicon glyph="shopping-cart" />
							</span>
						) : (
							name
						)}
					</td>
				) : (
					<td style={{ verticalAlign: 'middle' }} colSpan={this.state.editing ? 2 : 1}>
						<Form inline onSubmit={this.editDone}>
							<FormGroup style={{ marginBottom: '0px' }}>
								<InputGroup>
									<FormControl
										type="text"
										defaultValue={name}
										placeholder={name}
										onChange={this.handleChange}
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
									onChange={this.onSelectChange}
									inputRef={ref => (this.input = ref)}>
									{this.getCategoriesList()}
								</FormControl>
							</FormGroup>
						</Form>
					</td>
				)}
				{mode === 1 && !this.state.editing ? (
					<td>
						{' '}
						<Button onClick={this.editStart}>✎</Button>{' '}
					</td>
				) : null}
				{mode === 1 ? (
					<td>
						{' '}
						<Button bsStyle="warning" onClick={() => remove(id)}>
							X
						</Button>{' '}
					</td>
				) : null}
			</tr>
		);
	}
}

Item.propTypes = {
	name: PropTypes.string.isRequired,
	bought: PropTypes.bool.isRequired,
	starred: PropTypes.bool.isRequired,
	needed: PropTypes.bool.isRequired,
	id: PropTypes.number.isRequired,
	category: PropTypes.string.isRequired,
	mode: PropTypes.number.isRequired,
	toggleStarred: PropTypes.func.isRequired,
	toggleBought: PropTypes.func.isRequired,
	toggleNeeded: PropTypes.func.isRequired,
	remove: PropTypes.func.isRequired,
	rename: PropTypes.func.isRequired,
	changeCategory: PropTypes.func.isRequired,
	categories: PropTypes.arrayOf(
		PropTypes.shape({
			key: PropTypes.string.isRequired,
			value: PropTypes.string.isRequired,
		}).isRequired
	).isRequired,
};

export default Item;
