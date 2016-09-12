class GameList extends React.Component {
    constructor (props) {
        super(props);
        this.state = {picks: props.picks, games: props.games};
    }

    addNewPick (new_pick) {
        var picks = this.state.picks;
        var updated_pick = false;

        _.each(picks, function(pick){
            if (pick.game_id === new_pick.game_id) {
                pick.winner_id = new_pick.winner_id;
                updated_pick = true;
                new_pick = updated_pick;
            }
        })

        if (!updated_pick) {
            picks.push(new_pick);
            var request_type = 'POST';
        } else {
            var request_type = 'PUT';
        }

        this.sendPickRequest(new_pick, request_type, function(pick){
            var games = this.state.games;
            _.findWhere(games, {id: pick.game_id}).winner_id = pick.winner_id;
            this.setState({picks: picks, games: games});
        })
    }

    removePick (game_id) {
        var pick = _.findWhere(this.state.picks, {
            game_id: game_id
        });

        if (pick.id) {
            this.sendPickRequest(pick, 'DELETE', this.handleDeletePick.bind(this, pick));
        } else {
            this.handleDeletePick(pick);
        }
    }

    handleDeletePick (pick) {
        var picks = _.without(this.state.picks, pick);
        var games = this.state.games;
        _.findWhere(games, {id: game_id}).winner_id = null;

        this.setState({picks: picks, games: games});
    }

    sendPickRequest (pick, request_type, callback) {
        if (pick.id) {
            var url = this.props.url + '/' + pick.id
        } else {
            var url = this.props.url;
        }

        var _this = this;
        $.ajax({
            url: url,
            dataType: 'json',
            type: request_type,
            data: {
                pick: pick
            },
            success: function(data) {
                if (request_type === 'POST') {
                    var picks = _this.state.picks;
                    _.findWhere(picks, {game_id: data.game_id}).id = data.id;
                    _this.setState({picks: picks});
                }

                callback(pick);
            },
            error: function(xhr, status, err) {
                console.error(url, status, err.toString());
            }
        })
    }

    render () {
        var _this = this;
        var gameNodes = this.state.games.map(function(game) {
            return (
                <Game key={game.id} game={game} addNewPick={_this.addNewPick.bind(_this)} removePick={_this.removePick.bind(_this)} />
            );
        })
        return (
            <div>
                <h1>Games</h1>
                <table>
                    <tbody>
                        <tr>
                            <th>Home Team</th>
                            <th>Away Team</th>
                            <th>Spread</th>
                        </tr>
                        {gameNodes}
                    </tbody>
                </table>
            </div>
        );
    }
}