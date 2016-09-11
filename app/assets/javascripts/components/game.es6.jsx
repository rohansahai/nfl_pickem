class Game extends React.Component {
  render () {
    return (
      <tr>
        <td> {this.props.game.home_team.name} </td>
        <td> {this.props.game.away_team.name} </td>
        <td> {this.props.game.spread} </td>
      </tr>
    );
  }
}

Game.propTypes = {
  game: React.PropTypes.object
};
