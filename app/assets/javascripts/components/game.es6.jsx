class Game extends React.Component {
    render () {
        var home_team = this.props.game.home_team;
        var away_team = this.props.game.away_team;
        return (
            <tr className={this.getGamePickedClass()} onClick={this.handlePickSelect.bind(this)}>
                <td></td>
                <td className={this.getTeamSelectedClass(home_team.id) + " select-team"} data-team-id={home_team.id}> {home_team.name} </td>
                <td className={this.getTeamSelectedClass(home_team.id)}> {this.getSpreadPretty(true)} </td>
                <td className={this.getTeamSelectedClass(away_team.id) + " select-team"} data-team-id={away_team.id}> {away_team.name} </td>
                <td className={this.getTeamSelectedClass(away_team.id)}> {this.getSpreadPretty(false)} </td>
                <td> {this.getDatePretty()} </td>
            </tr>
        );
    }

    getTeamSelectedClass (winner_id) {
        if (winner_id === this.props.game.winner_id) {
            return 'team-selected';
        }

        return '';
    }

    getGamePickedClass () {
        if (this.props.game.winner_id) {
            return 'pick-active';
        }
    }

    getDatePretty () {
        var days_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'};
        var date = new Date(this.props.game.time);
        var day = days_map[date.getDay()];
        return day + " " + date.toLocaleTimeString();
    }

    getSpreadPretty (home) {
        var spread = (home) ? this.props.game.spread : this.props.game.spread * -1;
        if (spread > 0) {
            return "+" + spread;
        }
        return spread;
    }

    handlePickSelect (e) {
        var winner_id = $(e.target).data('team-id');

        // check if they are deselecting
        if (this.props.game.winner_id == winner_id) {
            this.props.removePick(this.props.game.id);
            return;
        }

        var _this = this;
        this.props.addNewPick({
            winner_id: winner_id,
            game_id: _this.props.game.id,
            week: _this.props.game.week
        });
    }
}

Game.propTypes = {
    game: React.PropTypes.object
};
