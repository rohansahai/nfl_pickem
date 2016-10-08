class Standings extends React.Component {
    render () {
        var _this = this;
        var userRecordNodes = this.getUserRecordNodes(JSON.parse(this.props.users));

        return (
            <div className="card weekly-picks-card">
                <div className="card-content">
                    <div className="row title-row">
                        <span className="card-title">Standings</span>
                    </div>

                    <table className="bordered">
                        <tbody>
                            <tr>
                                <th data-id="rank"></th>
                                <th>Name</th>
                                <th>Wins</th>
                                <th>Losses</th>
                                <th>Pushes</th>
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
        var last_rank_points = users[0].points;
        var last_rank = 1;

        return users.map(function(user, index) {
            if (last_rank_points === user.points ) {
                user.rank = last_rank;
            } else {
                user.rank = index + 1;
                last_rank_points = user.points;
                last_rank = index + 1;
            }

            return (
                <UserRecord key={user.id} user={user} />
            );
        });
    }
}