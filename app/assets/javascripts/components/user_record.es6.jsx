class UserRecord extends React.Component {
    render () {
        return (
            <tr>
                <td></td>
                <td> {this.props.user.name} </td>
                <td> {this.props.user.wins} </td>
                <td> {this.props.user.losses} </td>
                <td> {this.props.user.draws} </td>
                <td> {this.getPoints()} </td>
            </tr>
        );
    }

    getPoints () {
        return (this.props.user.wins * 3) + (this.props.user.draws * .5);
    }
}

UserRecord.propTypes = {
    user: React.PropTypes.object
};
