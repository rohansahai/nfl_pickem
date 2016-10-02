class Standings extends React.Component {
    render () {
        var _this = this;

        var users = JSON.parse(this.props.users);
        var userRecordNodes = users.map(function(user) {
            return (
                <UserRecord key={user.id} user={user} />
            );
        });

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
                                <th>Draws</th>
                                <th>Points</th>
                            </tr>
                            {userRecordNodes}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}