class Game extends React.Component {
    render () {
        var home_team = this.props.game.home_team;
        var away_team = this.props.game.away_team;
        return (
            <tr className={this.getGamePickedClass()} onClick={this.handlePickSelect.bind(this)}>
                <td><i className="game-icon material-icons">{this.getIcon()}</i></td>
                <td className={this.getTeamSelectedClass(home_team.id)}> {this.getSpreadPretty(true)} </td>
                <td className={this.getTeamSelectedClass(home_team.id) + " select-team"} data-team-id={home_team.id}> {home_team.name} </td>
                <td className={this.getTeamSelectedClass(away_team.id) + " select-team"} data-team-id={away_team.id}> {away_team.name} </td>
                <td> {this.getDatePretty()} </td>
            </tr>
        );
    }

    getIcon () {
        var game_winner_id = this.props.game.spread_winner_id;
        if ((game_winner_id || this.props.game.push) && this.props.game.pick) {
            var user_winner_id = this.props.game.pick.winner_id;
            if (this.props.game.push) {
                return 'thumbs_up_down';
            } else if (game_winner_id === user_winner_id) {
                return 'thumb_up';
            } else {
                return 'thumb_down';
            }
        }
        return (this.hasGameStarted()) ? 'lock_outline' : 'lock_open';
    }

    hasGameStarted () {
        var game_date = new Date(this.props.game.time);
        var now = new Date();

        return ((now - game_date) > 0) ? true : false;
    }

    getTeamSelectedClass (winner_id) {
        if (this.props.game.pick && winner_id === this.props.game.pick.winner_id) {
            return 'team-selected';
        }

        return '';
    }

    getGamePickedClass () {
        var game_winner_id = this.props.game.spread_winner_id;
        if ((game_winner_id || this.props.game.push) && this.props.game.pick) {
            var user_winner_id = this.props.game.pick.winner_id;
            if (this.props.game.push) {
                return 'pick-draw';
            } else if (game_winner_id === user_winner_id) {
                return 'pick-win';
            } else {
                return 'pick-loss';
            }
        }

        if (this.props.game.pick && this.props.game.pick.winner_id) {
            return 'pick-active';
        }
    }

    getDatePretty () {
        return moment(this.props.game.time).calendar();
    }

    getSpreadPretty (home) {
        var spread = (home) ? this.props.game.home_spread : this.props.game.home_spread * -1;
        if (spread > 0) {
            return "+" + spread;
        }
        return spread;
    }

    handlePickSelect (e) {
        var winner_id = $(e.target).data('team-id');

        // check if they are deselecting
        if (this.props.game.pick && this.props.game.pick.winner_id == winner_id) {
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
