class Topbar extends React.Component {
    getLeagues() {
        let leagues = this.props.current_user.leagues
        let leagueOptions = []
        // can use some sort of forEach here probably but I'm on a plane with no internet
        // forget javascript syntax
        for (let i = 0; i < leagues.length; i++) {
            leagueOptions.push(
                <li key={i} onClick={this.changeLeague.bind(this, leagues[i])}>
                    <a>{leagues[i].name}</a>
                </li>
            )
        }
        return leagueOptions
    }

    changeLeague(league) {
        $.ajax({
            url: '/change-league/' + league.id,
            type: 'GET',
            success: (data) => {
            },
            error: (data, status, err) => {
                this.handleErrors(data.responseJSON.errors);
            }
        })
    }

    render () {
        return (
            <nav>
                <div className="nav-wrapper">
                  <a href="https://www.superpickem.me/">
                    <img className="superPickemLogo" src='http://aroncey.com/nfl_pickemL/images/superpickem.png'></img>
                  </a>
                    <a href="#" className="brand-logo title"></a>
                    <ul id="nav-mobile" className="right hide-on-med-and-down">
                        <l1>
                            <a className='dropdown-button btn blue white-text darken-4' data-hover="true" data-activates='dropdown-leagues'>
                                Leagues
                            </a>
                            <ul id='dropdown-leagues' className='card-panel dropdown-content black-text text-darken-4'>
                                {this.getLeagues()}
                            </ul>
                        </l1>
                        <li><a href="/signout">Sign Out</a></li>
                    </ul>
                </div>
            </nav>
        );
    }
}
