import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Button, Form, FormGroup, InputGroup, FormControl } from 'react-bootstrap';

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

	translateCategory(category) {
		const categories = {};
		return categories.category;
	}

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
						<span> {needed ? <strong>🛒 {name}</strong> : name} </span>
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
										onBlur={this.editDone}
										autoFocus
									/>
									<InputGroup.Button>
										<Button type="submit" bsStyle="success">
											✓
										</Button>
									</InputGroup.Button>
								</InputGroup>
							</FormGroup>
						</Form>
					</td>
				)}
				<td>{this.translateCategory(category)}</td>

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
};

export default Item;
