class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  helper_method :current_user, :current_week, :current_league

  def current_league
    if !session[:league_id]
      session[:league_id] = LeaguesUser.where(user_id: current_user.id).first.league.id
    end
    @current_league ||= League.find(session[:league_id])
  end

  def current_user
    return unless session[:user_id]
    @current_user ||= User.find(session[:user_id])
  end

  def is_user_logged_in
    redirect_to "/auth/google_oauth2" if current_user.nil?
  end

  def current_week
    # get the earliest game with no result, that should be the active week
    # otherwise return the last completed game's week
    unfinished_games = Game.where(:moneyline_winner_id => nil)
    if (unfinished_games.empty?)
      return Game.order("time DESC").limit(1).first.week
    else
      return unfinished_games.order("time DESC").limit(1).first.week
    end
  end
end
