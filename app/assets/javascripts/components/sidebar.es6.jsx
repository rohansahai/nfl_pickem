class Sidebar extends React.Component {
    render () {
        return (
            <div id="sidebar">
                <ul>
                    <li className="active">
                        <i className="material-icons">schedule</i>
                        <span>This Week's Picks</span>
                    </li>
                    <li>
                        <i className="material-icons">skip_previous</i>
                        <span>Previous Picks</span>
                    </li>
                    <li> 
                        <i className="material-icons">star</i>
                        <span>League Standings</span>
                    </li>
                </ul>
            </div>
        );
    }
}