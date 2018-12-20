import React, { PureComponent } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Button, Form, FormGroup, InputGroup, FormControl, ControlLabel } from 'react-bootstrap';

import Actions from '../actions/Actions';
import CategoriesSelector from './CategoriesSelector.jsx';

class AddItemForm extends PureComponent {
	state = { name: '', category: 'other' };
	inputId = 'newItemInput';

	handleSubmit = event => {
		const { name, category } = this.state;
		const { items, mode, addItem } = this.props;

		event.preventDefault();
		const foundItem = items.find(el => el.name.toLowerCase() === name.toLowerCase());
		if (!foundItem) {
			const needed = mode === 2;
			addItem(name, needed, category);
		}
		this.setState({ name: '' });
		this.setFocutOnInput();
	};

	handleInputChange = event => {
		this.setState({ name: event.target.value });
	};

	handleSelectorChange = event => {
		this.setState({ category: event.target.value });
	};

	setFocutOnInput = () => {
		document.getElementById(inputId).focus();
	};

	componentDidMount() {
		document.addEventListener('keydown', this.setFocutOnInput, false);
	}

	render() {
		const { name, category } = this.state;
		const { categories } = this.props;
		const { inputId, handleSubmit, handleInputChange, handleSelectorChange } = this;
		return (
			<Form inline onSubmit={handleSubmit}>
				<FormGroup>
					<InputGroup>
						<FormControl
							id={inputId}
							type="text"
							value={name}
							placeholder="Новый продукт"
							onChange={handleInputChange}
						/>
						<InputGroup.Button>
							<Button bsStyle="primary" type="submit">
								Добавить
							</Button>
						</InputGroup.Button>
					</InputGroup>
					<CategoriesSelector
						onSelectChange={handleSelectorChange}
						category={category}
						categories={categories}
					/>
				</FormGroup>
			</Form>
		);
	}
}

const mapStateToProps = state => ({
	mode: state.mode,
	items: state.items,
	categories: state.categories,
});

const mapDispatchToProps = dispatch => ({
	addItem: bindActionCreators(Actions.addItem, dispatch),
});

AddItemForm = connect(
	mapStateToProps,
	mapDispatchToProps
)(AddItemForm);

export default AddItemForm;
