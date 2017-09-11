class UserRecord extends React.Component {
    render () {
        var previous_picks_url = "/users/" + this.props.user.id + "/picks";
        return (
            <tr className={(window.current_user.id === this.props.user.id) ? 'current-user' : ''}>
                <td className="user-ranking"> {this.props.user.rank} </td>
                <td> <a href={previous_picks_url}> {this.props.user.name} </a> </td>
                <td> {this.props.user.wins} </td>
                <td> {this.props.user.losses} </td>
                <td> {this.props.user.pushes} </td>
                <td> {this.props.user.percent} </td>
                <td> {this.props.user.points} </td>
            </tr>
        );
    }
}

UserRecord.propTypes = {
    user: React.PropTypes.object
};
