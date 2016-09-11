class Game extends React.Component {
    render () {
        return (
            <tr className={this.getPickedTeamLocation()} onClick={this.handlePickSelect.bind(this)}>
                <td data-team-id={this.props.game.home_team.id}> {this.props.game.home_team.name} </td>
                <td data-team-id={this.props.game.away_team.id}> {this.props.game.away_team.name} </td>
                <td> {this.props.game.spread} </td>
            </tr>
        );
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
        this.props.onPickSelect();
    }
}

Game.propTypes = {
    game: React.PropTypes.object
};
