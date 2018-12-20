import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import {
	Button,
	Form,
	FormGroup,
	InputGroup,
	FormControl,
	ControlLabel,
	Glyphicon,
} from 'react-bootstrap';

import CategoriesSelector from './CategoriesSelector.jsx';

class Item extends PureComponent {
	state = {
		editing: false,
		name: this.props.name,
		defaultName: this.props.name,
	};

	style = {
		td: {
			verticalAlign: 'middle',
			whiteSpace: 'normal',
		},
		td_not_editing: {
			paddingLeft: '20px',
		},
		form_group: {
			marginBottom: '0px',
		},
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

	handleInputChange = event => {
		this.setState({ name: event.target.value });
	};

	handleSelectorChange = event => {
		this.props.changeCategory(this.props.id, event.target.value);
	};

	componentWillReceiveProps(nextProps) {
		if (nextProps.mode !== this.props.mode) {
			this.setState({ editing: false });
		}
	}

	handleClick = () => {
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
		const { name, needed, bought, id, category, categories, mode, remove } = this.props;
		const {
			style,
			editDone,
			handleInputChange,
			handleSelectorChange,
			editStart,
			getCategoriesList,
			handleClick,
		} = this;
		const editing = this.state.editing;

		return (
			<tr className={category + (mode === 2 && bought ? ' bought' : '')}>
				{!editing ? (
					<td style={{ ...style.td, ...style.td_not_editing }} onClick={handleClick}>
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
					<td style={style.td} colSpan="2">
						<Form inline onSubmit={editDone}>
							<FormGroup style={style.form_group}>
								<InputGroup>
									<FormControl
										type="text"
										defaultValue={name}
										placeholder={name}
										onChange={handleInputChange}
										autoFocus
									/>
									<InputGroup.Button>
										<Button type="submit" bsStyle="success">
											✓
										</Button>
									</InputGroup.Button>
								</InputGroup>{' '}
								<CategoriesSelector
									onSelectChange={handleSelectorChange}
									category={category}
									categories={categories}
								/>
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
	setNeeded: PropTypes.func.isRequired,
	setNotNeeded: PropTypes.func.isRequired,
	setBought: PropTypes.func.isRequired,
	setNotBought: PropTypes.func.isRequired,
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
