import React from 'react';

import TableContainer from '../containers/TableContainer.jsx';

const DesktopComponent = () => (
    <div className="desktop-block">
        <div className="desktop-block__block">
            <h3 className="desktop-block__header">{'Составление'}</h3>
            <TableContainer mode={1} />
        </div>

        <div className="desktop-block__block">
            <h3 className="desktop-block__header">{'Покупка'}</h3>
            <TableContainer mode={2} />
        </div>
    </div>
);

export default DesktopComponent;
