class UserRecord extends React.Component {
    render () {
        return (
            <tr>
                <td></td>
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
