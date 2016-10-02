class Topbar extends React.Component {
    render () {
        if (this.props.current_user) {
            var session_link = '/signout';
            var session_link_text = 'Sign Out';
        } else {
            var session_link = '/auth/google_oauth2';
            var session_link_text = 'Sign In';
        }
        return (
            <nav>
                <div className="nav-wrapper">
                    <a href="#" className="brand-logo title">Pick'em</a>
                    <ul id="nav-mobile" className="right hide-on-med-and-down">
                        <li><a href={session_link}>{session_link_text}</a></li>
                    </ul>
                </div>
            </nav>
        );
    }
}