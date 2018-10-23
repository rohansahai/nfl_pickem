class LeaguesController < ApplicationController
  before_action :is_user_logged_in

  def change_league
    league_id = params[:league_id]
    # Will throw an unfriendly error if user is not in league
    league = user.leagues.find(league_id)
    session[:league_id] = league.id

    redirect_to root_path
  end
end
