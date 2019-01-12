import React from 'react';
import PropTypes from 'prop-types';

import ModeSelector from './ModeSelector.jsx';
import TableContainer from '../containers/TableContainer.jsx';

const MobileComponent = ({ mode, selectMode }) => (
    <div>
        <ModeSelector mode={mode} selectMode={selectMode} />
        <TableContainer mode={mode} />
    </div>
);

MobileComponent.propTypes = {
    mode: PropTypes.number.isRequired,
    selectMode: PropTypes.func.isRequired,
};

export default MobileComponent;
