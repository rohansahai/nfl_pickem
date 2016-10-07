class Sidebar extends React.Component {
    render () {
        return (
            <div id="sidebar">
                <ul>
                    <li className={this.isActive('picks') && "active"}>
                        <a href="/picks">
                            <i className="material-icons">schedule</i>
                            <span>This Week's Picks</span>
                        </a>
                    </li>
                    <li className={this.isActive('previous') && "active"}>
                        <a href="/previous">
                            <i className="material-icons">skip_previous</i>
                            <span>Previous Picks</span>
                        </a>
                    </li>
                    <li className={this.isActive('standings') && "active"}> 
                        <a href="/standings">
                            <i className="material-icons">star</i>
                            <span>League Standings</span>
                        </a>
                    </li>
                </ul>
            </div>
        );
    }

    isActive (route) {
        if (window.location.pathname.indexOf(route) > -1) {
            return true;
        }

        return false;
    }
}