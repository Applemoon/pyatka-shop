import React, { PureComponent } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Button, Form, FormGroup, InputGroup, FormControl } from 'react-bootstrap';

import Actions from '../actions/Actions';

class AddItemForm extends PureComponent {
	state = { value: '' };

	handleSubmit = event => {
		event.preventDefault();
		const foundItem = this.props.items.find(
			el => el.name.toLowerCase() === this.state.value.toLowerCase()
		);
		if (!foundItem) {
			const needed = this.props.mode === 2;
			this.props.addItem(this.state.value, needed);
		}
		this.setState({ value: '' });
	};

	handleChange = event => {
		this.setState({ value: event.target.value });
	};

	onKeyPress = () => {
		if (!document.hasFocus()) document.getElementById('newItemInput').focus();
	};

	componentDidMount() {
		document.addEventListener('keydown', this.onKeyPress, false);
	}

	render() {
		return (
			<Form inline onSubmit={this.handleSubmit}>
				<FormGroup>
					<InputGroup>
						<FormControl
							id="newItemInput"
							type="text"
							value={this.state.value}
							placeholder="Новый продукт"
							onChange={this.handleChange}
						/>
						<InputGroup.Button>
							<Button bsStyle="primary" type="submit">
								Добавить
							</Button>
						</InputGroup.Button>
					</InputGroup>
				</FormGroup>
			</Form>
		);
	}
}

const mapStateToProps = state => ({
	mode: state.mode,
	items: state.items,
});

const mapDispatchToProps = dispatch => ({
	addItem: bindActionCreators(Actions.addItem, dispatch),
});

AddItemForm = connect(
	mapStateToProps,
	mapDispatchToProps
)(AddItemForm);

export default AddItemForm;
