class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  helper_method :current_user, :current_week

  def current_user
    # return unless session[:user_id]
    # @current_user ||= User.find(session[:user_id])
    @current_user = User.find(26)
  end

  def is_user_logged_in
    # redirect_to "/auth/google_oauth2" if current_user.nil?
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
