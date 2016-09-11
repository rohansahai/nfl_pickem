class GamesController < ApplicationController
  def index
    @games = Game.where(:week => params[:week_id])
                 .includes([:home_team, :away_team])
                 .as_json(:include => [:home_team, :away_team])

    @picks = current_user.picks.where(:week => params[:week_id])

    @games.each do |game|
      pick = @picks.find_by(:game_id => game['id'])
      if (pick)
        game['picked_team_location'] = (game['home_team_id'] == pick['winner_id']) ? 'home' : 'away'
      end
    end

    render component: 'GameList', props: { games: @games, picks: @picks }, class: 'game_list'
  end
end
