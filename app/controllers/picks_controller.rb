class PicksController < ApplicationController
  before_action :is_user_logged_in

  def index
    @user = User.find(params[:user_id])
    @picks = @user
              .picks
              .includes([:game => [:home_team, :away_team]])
    @weeks = (1...current_week+1).to_a.reverse
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

  def previous
    @picks = current_user
              .picks
              .includes([:game => [:home_team, :away_team]])
    @weeks = (1...current_week+1).to_a.reverse
    render "index"
  end

  def standings
    skip = [64, 65, 66]
    @users = User.where.not(id: skip).all.to_a.sort_by(&:points).reverse.to_json(:methods => [:wins, :losses, :pushes, :percent, :points])
  end

  def distribution
    @distribution_hash = {}
    current_week.downto(1).each do |week|
      @distribution_hash[week] = []
      picks = Pick.joins(:game).where(:week => week).where("games.time < ?", Time.now)
      weekly_distro = picks.group(:game_id, :winner_id).count.sort_by {|k, v| v}.reverse.to_h
      weekly_distro.each do |key, pick_count|
        pick = Pick.find_by(:week => week, :winner_id => key[1])
        game = Game.find(key[0])

        if game.home_team_id == pick.winner_id
          opponent_id = game.away_team_id
          spread = game.home_spread
        else
          opponent_id = game.home_team_id
          spread = game.home_spread * -1
        end
        @distribution_hash[week].push({
          :count => pick_count,
          :winner => Team.find(key[1]),
          :opponent => Team.find(opponent_id),
          :result => pick.result,
          :game => game,
          # :logo => game.logo_path,
          :spread => spread
        })
      end
    end
  end

  private
  def pick_params
    params.require(:pick).permit(:id, :game_id, :winner_id, :week)
  end
end
