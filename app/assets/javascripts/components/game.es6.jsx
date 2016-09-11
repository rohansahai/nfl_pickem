class Game extends React.Component {
    render () {
        return (
            <tr className={this.props.game.picked_team_location} onClick={this.handlePickSelect.bind(this)}>
                <td> {this.props.game.home_team.name} </td>
                <td> {this.props.game.away_team.name} </td>
                <td> {this.props.game.spread} </td>
            </tr>
        );
    }

    handlePickSelect (e) {
        this.props.onPickSelect();
    }
}

Game.propTypes = {
    game: React.PropTypes.object
};
