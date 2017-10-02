class Standings extends React.Component {
    componentWillMount () {
        this.setState({week: 'all'})
    }

    render () {
        var _this = this;
        var userRecordNodes = this.getUserRecordNodes(JSON.parse(this.props.users));

        return (
            <div className="card weekly-picks-card">
                <div className="card-content">
                    <div className="row title-row">
                        <span className="card-title">Standings</span>
                        <a className='dropdown-button btn' href='#' data-activates='dropdown1'>Week</a>
                          <ul id='dropdown1' className='dropdown-content'>
                            <li><a href="#!">1</a></li>
                            <li><a href="#!">2</a></li>
                            <li><a href="#!">3</a></li>
                          </ul>
                    </div>
                    <table className="bordered">
                        <tbody>
                            <tr>
                                <th data-id="rank"></th>
                                <th>Name</th>
                                <th>Wins</th>
                                <th>Losses</th>
                                <th>Pushes</th>
                                <th>Win Rate (%)</th>
                                <th>Points</th>
                            </tr>
                            {userRecordNodes}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }

    getUserRecordNodes (users) {
        var week = this.state.week

        // sort users
        users.sort((a, b) => {
            return b.week_standings[week].points - a.week_standings[week].points
        })

        // modify user objects for user record component
        var last_rank_points = users[0].week_standings[week].points;
        var last_rank = 1;

        return users.map(function(user, index) {
            if (week != 'all') {
                user = Object.assign(user, user.week_standings[week])
            }

            if (last_rank_points === user.points ) {
                user.rank = last_rank;
            } else {
                user.rank = index + 1;
                last_rank_points = user.points;
                last_rank = index + 1;
            }

            return (
                <UserRecord key={user.id} user={user}/>
            );
        });
    }
}
