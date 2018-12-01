import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import Error from './Error.jsx';
import ModeSelector from './ModeSelector.jsx';
import TableContainer from '../containers/TableContainer.jsx';
import AddItemForm from './AddItemForm.jsx';
import Actions from '../actions/Actions';
import OfflineWarning from '../components/OfflineWarning.jsx';

class App extends PureComponent {
    componentDidMount() {
        this.props.loadItems();
    }

    render() {
        const { items, error, mode, offline, loading, selectMode } = this.props;

        return error ? (
            <Error />
        ) : loading ? (
            <p>Загрузка...</p>
        ) : (
            <div>
                {offline && <OfflineWarning />}
                <ModeSelector mode={mode} selectMode={selectMode} />
                <TableContainer />
                <AddItemForm items={items} />
            </div>
        );
    }
}

const mapStateToProps = state => ({
    items: state.items,
    error: state.error,
    mode: state.mode,
    offline: state.offline,
    loading: state.loading,
});

const mapDispatchToProps = dispatch => ({
    selectMode: bindActionCreators(Actions.selectMode, dispatch),
    loadItems: bindActionCreators(Actions.loadItems, dispatch),
});

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(App);
