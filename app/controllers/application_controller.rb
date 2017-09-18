class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  helper_method :current_user, :current_week

  def current_user
    return unless session[:user_id]
    @current_user ||= User.find(session[:user_id])
    # @current_user = User.find(2)
    # if @current_user.id == 65 or @current_user.id == 66
    #   @current_user = User.find(50)
    # elsif @current_user.id == 64
    #   @current_user = User.find(24)
    # end
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
