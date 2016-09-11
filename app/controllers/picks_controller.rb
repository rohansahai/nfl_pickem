class PicksController < ApplicationController
  def create
    pick = current_user.picks.create({
      :game_id => pick_params[:game_id],
      :winner_id => pick_params[:winner_id],
      :week => pick_params[:week]
    })

    render json: pick, status: 200
  end

  def update
    pick = current_user.picks.find(pick_params[:id])
    pick.update(:winner_id => pick_params[:winner_id])
    render json: pick, status: 200
  end

  def destroy
    pick = current_user.picks.find(pick_params[:id])
    pick.destroy
    render json: pick, status: 200 
  end

  def pick_params
    params.require(:pick).permit(:id, :game_id, :winner_id, :week)
  end
end
