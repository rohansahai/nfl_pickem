class Game extends React.Component {
    render () {
        return (
            <tr className={this.getPickedTeamLocation()} onClick={this.handlePickSelect.bind(this)}>
                <td data-team-id={this.props.game.home_team.id}> {this.props.game.home_team.name} </td>
                <td data-team-id={this.props.game.away_team.id}> {this.props.game.away_team.name} </td>
                <td> {this.props.game.spread} </td>
                <td> {this.getDatePretty()} </td>
            </tr>
        );
    }

    getDatePretty () {
        var days_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'};
        var date = new Date(this.props.game.time);
        var day = days_map[date.getDay()];
        return day + " " + date.toLocaleTimeString();
    }

    getPickedTeamLocation () {
        if (!this.props.game.winner_id) {
            return '';
        }

        if (this.props.game.home_team.id == this.props.game.winner_id) {
            return 'home';
        } else {
            return 'away';
        }
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
