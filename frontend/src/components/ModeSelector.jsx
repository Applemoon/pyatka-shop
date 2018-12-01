import React from 'react';
import { Nav, NavItem } from 'react-bootstrap';
import PropTypes from 'prop-types';

const style = { paddingBottom: '20px' };

const ModeSelector = ({ mode, selectMode }) => (
	<Nav bsStyle="pills" activeKey={mode} onSelect={key => selectMode(key)} style={style}>
		<NavItem disabled> Режимы: </NavItem>
		<NavItem eventKey={1}> Составить список </NavItem>
		<NavItem eventKey={2}> В магазине </NavItem>
	</Nav>
);

ModeSelector.propTypes = {
	mode: PropTypes.number.isRequired,
	selectMode: PropTypes.func.isRequired
};

export default ModeSelector;
