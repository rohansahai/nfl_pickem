class GameList extends React.Component {
    constructor (props) {
        super(props);
        this.state = {picks: props.picks, games: props.games};
    }

    addNewPick (new_pick) {
        var request_type = (new_pick.id) ? 'PUT' : 'POST';

        var _this = this;
        this.sendPickRequest(new_pick, request_type, function(pick){
            var picks = _this.state.picks;
            if (request_type === 'POST') {
                picks.push(pick);
            } else {
                _.findWhere(picks, {id: pick.id}).winner_id = pick.winner_id;
            }

            var games = _this.state.games;
            _.findWhere(games, {id: pick.game_id}).winner_id = pick.winner_id;
            _this.setState({picks: picks, games: games})
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
        _.findWhere(games, {id: pick.game_id}).winner_id = null;

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
                callback(data);
            },
            error: function(data, status, err) {
                _this.handleErrors(data.responseJSON.errors);
            }
        })
    }

    handleErrors (errors) {
        var error_message = "";
        _.each(errors, function(val, key){
            error_message += "Errors with " + key + ":\n";
            _.each(val, function(msg){
                error_message +=  "  -" + msg + "\n";
            })
        })

        alert(error_message);
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