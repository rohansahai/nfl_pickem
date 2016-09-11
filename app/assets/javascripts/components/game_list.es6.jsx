class GameList extends React.Component {
    render () {
        // go through games and add property for picked team if exists?
        // var pick = _.findWhere(this.props.picks, {game_id: this.props.game.id});
        var _this = this;
        var gameNodes = this.props.games.map(function(game) {
            return (
                <Game key={game.id} game={game} picks={_this.props.picks} />
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