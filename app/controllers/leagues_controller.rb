class LeaguesController < ApplicationController
  before_action :is_user_logged_in, except: [:league_invite]

  def change_league
    league_id = params[:league_id]
    # Will throw an unfriendly error if user is not in league
    league = current_user.leagues.find(league_id)
    session[:league_id] = league.id

    redirect_to root_path
  end

  # I'm well aware this is easily exploitable and anyone can invite themselves to a league
  # but not too concerned about this seeing as we have one league at the time of writing
  # this. Lol.
  def league_invite
    league_id = params[:league_id]
    # This won't fail very nicely if no league found.
    league = League.find(league_id)
    session[:invited_league_id] = league.id

    redirect_to "/auth/google_oauth2"
  end
end
