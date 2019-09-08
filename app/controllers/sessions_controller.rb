class SessionsController < ApplicationController
  def create
    league_to_join_id = session[:invited_league_id]
    session[:invited_league_id] = nil

    user = User.from_omniauth(env["omniauth.auth"], league_to_join_id)
    if user
      session[:user_id] = user.id
      session[:league_id] = league_to_join_id || user.leagues.first.id
      redirect_to root_path
    else
      render json: {
        :errors => 'League sign up closed! (or maybe you chose the wrong google account)'
      }, status: 400
    end
  end

  def destroy
    session[:user_id] = nil
    session[:league_id] = nil
    session[:invited_league_id] = nil # just in case, shouldn't affect anything
    redirect_to root_path
  end
end
