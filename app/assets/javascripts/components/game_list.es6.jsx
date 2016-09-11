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
                updated_pick = pick;
            }
        })

        if (!updated_pick) {
            picks.push(new_pick);
            this.sendPickRequest(new_pick, 'POST');
        } else {
            this.sendPickRequest(updated_pick, 'PUT');
        }

        var games = this.state.games;
        _.findWhere(games, {id: new_pick.game_id}).winner_id = new_pick.winner_id;
        this.setState({picks: picks, games: games});
    }

    removePick (game_id) {
        var pick = _.findWhere(this.state.picks, {
            game_id: game_id
        })
        var picks = _.without(this.state.picks, pick);

        var games = this.state.games;
        _.findWhere(games, {id: game_id}).winner_id = null;

        this.setState({picks: picks, games: games});
        if (pick.id) {
            this.sendPickRequest(pick, 'DELETE');
        }
    }

    sendPickRequest (pick, request_type) {
        if (pick.id) {
            var url = this.props.url + '/' + pick.id
        } else {
            var url = this.props.url;
        }

        $.ajax({
            url: url,
            dataType: 'json',
            type: request_type,
            data: {
                pick: pick
            },
            success: function(daeta) {
                console.log('success!');
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