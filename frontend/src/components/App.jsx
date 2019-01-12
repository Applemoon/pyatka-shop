import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import Error from './Error.jsx';
import ModeSelector from './ModeSelector.jsx';
import TableContainer from '../containers/TableContainer.jsx';
import AddItemForm from './AddItemForm.jsx';
import Actions from '../actions/Actions';
import OfflineWarning from '../components/OfflineWarning.jsx';
import MobileComponent from '../components/MobileComponent.jsx';
import DesktopComponent from '../components/DesktopComponent.jsx';

class App extends PureComponent {
    componentDidMount() {
        this.props.loadData();
    }

    render() {
        const { items, error, mode, offline, loading, selectMode } = this.props;
        const isMobile = window.innerWidth <= 600;

        return error ? (
            <Error />
        ) : loading ? (
            <p>Загрузка...</p>
        ) : (
            <div>
                {offline && <OfflineWarning />}
                {isMobile ? (
                    <MobileComponent mode={mode} selectMode={selectMode} />
                ) : (
                    <DesktopComponent />
                )}
                <AddItemForm items={items} forceNeeded={mode === 2} />
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
    loadData: bindActionCreators(Actions.loadData, dispatch),
});

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(App);
