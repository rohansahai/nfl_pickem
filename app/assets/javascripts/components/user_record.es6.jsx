class UserRecord extends React.Component {
    render () {
        return (
            <tr className={(window.current_user.id === this.props.user.id) ? 'current-user' : ''}>
                <td className="user-ranking"> {this.props.user.rank} </td>
                <td> {this.props.user.name} </td>
                <td> {this.props.user.wins} </td>
                <td> {this.props.user.losses} </td>
                <td> {this.props.user.draws} </td>
                <td> {this.props.user.points} </td>
            </tr>
        );
    }
}

UserRecord.propTypes = {
    user: React.PropTypes.object
};
