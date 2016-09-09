class GamesController < ApplicationController
  def index
    @games = Game.where(:week => params[:week_id])
  end
end
