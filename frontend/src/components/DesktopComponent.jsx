import React from 'react';

import TableContainer from '../containers/TableContainer.jsx';

const DesktopComponent = () => (
    <div className="desktop-div">
        <div className="desktop-table-div">
            {'Составление'}
            <TableContainer mode={1} />
        </div>
        <div className="desktop-table-div">
            {'Покупка'}
            <TableContainer mode={2} />
        </div>
    </div>
);

export default DesktopComponent;
