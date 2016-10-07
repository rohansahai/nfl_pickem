class PicksController < ApplicationController
  before_action :is_user_logged_in

  def index
    @picks = current_user.picks.includes([:game])
    @weeks = (1...current_week).to_a
  end

  def create
    pick = current_user.picks.create({
      :game_id => pick_params[:game_id],
      :winner_id => pick_params[:winner_id],
      :week => pick_params[:week]
    })

    if pick.valid?
      render json: pick, status: 200
    else
      render json: {:errors => pick.errors}, status: 400
    end
  end

  def update
    pick = current_user.picks.find(pick_params[:id])
    pick.update(:winner_id => pick_params[:winner_id])
    if pick.valid?
      render json: pick, status: 200
    else
      render json: {:errors => pick.errors}, status: 400
    end
  end

  def destroy
    pick = current_user.picks.find(pick_params[:id])
    if pick.valid?
      pick.destroy
      render json: pick, status: 200 
    else
      render json: {:errors => pick.errors}, status: 400
    end
  end

  def standings
    @users = User.all.to_json(:methods => [:wins, :losses, :draws, :points])
  end

  private
  def pick_params
    params.require(:pick).permit(:id, :game_id, :winner_id, :week)
  end
end
