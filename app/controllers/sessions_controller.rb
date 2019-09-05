class SessionsController < ApplicationController
  def create
    user = User.from_omniauth(env["omniauth.auth"])
    if user
      session[:user_id] = user.id
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
    redirect_to root_path
  end
end
