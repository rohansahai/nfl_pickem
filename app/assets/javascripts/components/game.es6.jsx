class Game extends React.Component {
  render () {
    return (
      <tr data-game-id="">
        <td class="pick-team" data-team-id="">{this.props.homeTeam}</td>
        <td class="pick-team" data-team-id="">{this.props.awayTeam}</td>
        <td>{this.props.spread}</td>
      </tr>
    );
  }
}

Game.propTypes = {
  homeTeam: React.PropTypes.string,
  awayTeam: React.PropTypes.string,
  spread: React.PropTypes.node
};
