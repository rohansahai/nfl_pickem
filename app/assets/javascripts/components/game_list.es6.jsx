class GameList extends React.Component {
    constructor (props) {
        super(props);
        this.state = {picks: props.picks, games: props.games};
    }

    handlePickSelect (new_pick) {
        var picks = this.state.picks;
        var updated_pick = false;

        _.each(picks, function(pick){
            if (pick.game_id === new_pick.game_id) {
                pick.winner_id = new_pick.winner_id;
                updated_pick = true;
            }
        })

        if (!updated_pick) {
            picks.push(new_pick);
        }

        var games = this.state.games;
        _.findWhere(games, {id: new_pick.game_id}).winner_id = new_pick.winner_id;
        this.setState({picks: picks, games: games});
    }

    render () {
        var _this = this;
        var gameNodes = this.state.games.map(function(game) {
            return (
                <Game key={game.id} game={game} onPickSelect={_this.handlePickSelect.bind(_this)} />
            );
        })
        return (
            <div className="gameList">
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