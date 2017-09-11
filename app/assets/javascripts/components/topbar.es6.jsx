class Topbar extends React.Component {
    render () {
        return (
            <nav>
                <div className="nav-wrapper">
                    <a href="#" className="brand-logo title">Super Pick'em</a>
                    <ul id="nav-mobile" className="right hide-on-med-and-down">
                        <li><a href="/signout">Sign Out</a></li>
                    </ul>
                </div>
            </nav>
        );
    }
}
