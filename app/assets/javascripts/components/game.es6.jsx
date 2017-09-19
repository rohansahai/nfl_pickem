// import Homelogo from 'app/assets/javascripts/homelogo';
class Game extends React.Component {

    render () {
        var home_team = this.props.game.home_team;
        var homeLogo =  this.props.game.logo;
          var home_logoSrc = this.props.game.home_team.logoSrc
        var away_team = this.props.game.away_team;
          var away_logoSrc = this.props.game.away_team.logoSrc
        var awayLogo = this.props.game.awayLogo;

        return (
          // <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
            <tr className={this.getGamePickedClass()} onClick={this.handlePickSelect.bind(this)}>
                <td><i className="game-icon material-icons">{this.getIcon()}</i></td>
                <td className={this.getTeamSelectedClass(home_team.id)}> {this.getSpreadPretty(true)} </td>
                <td id="homeLogo" className={this.getHomeLogoClass(true)}>
                    <img src={home_team.logo_path} className="logos"  />
                </td>
                <td className={this.getTeamSelectedClass(home_team.id) + " select-team"} data-team-id={home_team.id}> {home_team.name} </td>
                <td className="center">{this.getScorePretty()}</td>
                <td id="awayLogo" className={this.getAwayLogoClass(true)}>
                    <img src={away_team.logo_path} className="logos" />
                </td>
                <td className={this.getTeamSelectedClass(away_team.id) + " select-team"} data-team-id={away_team.id}> {away_team.name} </td>
                <td> {this.getDatePretty()} </td>
            </tr>
        );
    }

///arthur
whoIsTheHomeTeam(home_team){
  // console.log(home_team)
    //   function img(){
    //     var image = document.createElement('img')
    //     image.src = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Atlanta_Falcons_logo.svg/1080px-Atlanta_Falcons_logo.svg.png";
    //     image.height = '10px'
    //     image.width = '10px'
     //
    //   //  var img = new Image(1,1); // width, height values are optional params
    //   //  img.src = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Atlanta_Falcons_logo.svg/1080px-Atlanta_Falcons_logo.svg.png";
    //   // return <img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Atlanta_Falcons_logo.svg/1080px-Atlanta_Falcons_logo.svg.png" height='90px' width='90px'></img>;
    //  }

      if(home_team.name==='Los Angeles Chargers'){
          console.log('greenBay')
          console.log(home_team.logo_path)
          return home_team.name;
          //React.renderComponent(<Img />, document.querySelector('#homeLogo'));
        //  ReactDOM.render(element,document.getElementById('homeLogo'))
      }else if (home_team.name==='New Orleans Saints') {
      console.log(home_team.name)
        return home_team.name +"NOLA";
      }else {

      }
    }

//  img(){
//   var img = new Image(1,1); // width, height values are optional params
//   img.src = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Atlanta_Falcons_logo.svg/1080px-Atlanta_Falcons_logo.svg.png";
//   return img;
// }

  whoIsTheAwayTeam(away_team){
    return away_team.name
  }
  getHomeLogoClass(){
  }
  getAwayLogoClass(){

  }
  //   var teamsID = {1: "Arizona Cardinals",
  // 2: "Atlanta Falcons" ,
  // 3 : "Baltimore Ravens",
  // 4 : "Buffalo Bills",
  // 5 : "Carolina Panthers",
  // 6 : "Chicago Bears",
  // 7 : "Cincinnati Bengals",
  // 8 : "Cleveland Browns",
  // 9 : "Dallas Cowboys",
  // 10 : "Denver Broncos",
  // 11 : "Detroit Lions",
  // 12 : "Green Bay Packers",
  // 13 :"Houston Texans",
  // 14 : "Indianapolis Colts",
  // 15 : "Jacksonville Jaguars",
  // 16 : "Kansas City Chiefs",
  // 17 : "Los Angeles Chargers",
  // 18 : "Los Angeles Rams",
  // 19 : "Miami Dolphins",
  // 20 : Minnesota Vikings,
  // 21 : New England Patriots,
  // 22 : New Orleans Saints,
  // 23 : New York Giants,
  // 24 : New York Jets,
  // 25 : Oakland Raiders,
  // 26 : Philadelphia Eagles,
  // 27 : Pittsburgh Steelers,
  // 28 : San Francisco 49ers,
  // 29 : Seattle Seahawks,
  // 30 : Tampa Bay Buccaneers,
  // 31 : Tennessee Titans,
  // 32 : Washington Redskins
  // }
    // debugger
    // console.log('home_team')

  whoIsTheAwayTeam(away_team){
    return away_team.name
  }
    // getHomeLogo() {
    //   // var img = new Image(1,1); // width, height values are optional params
    //   // img.src = 'http://content.sportslogos.net/logos/7/177/full/kwth8f1cfa2sch5xhjjfaof90.png';
    //   console.log("function getHomeLogo() ran")
    //   var homeImg = this.props.game.homeLogo;
    //   // return img;
    // }
    // getAwayLogo(){
    //   var awaryLogo = this.props.game.img;
    //   return this.awayLogo;
    // }
  getHomeLogoClass(){
  }
  getAwayLogoClass(){

  }

  getScorePretty () {
    var homeScore = this.props.game.home_team_score;
    var awayScore = this.props.game.away_team_score;
    if (homeScore || awayScore || homeScore === 0 || awayScore === 0) {
      return homeScore + " - " + awayScore
    }
    // else (homeScore == 0 || awayScore == 0)
  }
  /////////////////
  getSpreadPretty (home) {
      var spread = (home) ? this.props.game.home_spread : this.props.game.home_spread * -1;
      if (spread > 0) {
          return "+" + spread;
      }
      return spread;
  }
  getTeamSelectedClass (winner_id) {
      if (this.props.game.pick && winner_id === this.props.game.pick.winner_id) {
          return 'team-selected';
      }

      return '';
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

  get

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
    var gameStatus = this.props.game.game_status;
    return (this.hasGameStarted()) ? gameStatus : moment(this.props.game.time).format('ddd. MMM. DD h:mm A');
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
