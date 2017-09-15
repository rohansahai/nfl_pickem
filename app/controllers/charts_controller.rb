class ChartsController < ApplicationController
  def distribution
    distribution_hash = {}
    picks = Pick.joins(:game).where(:week => current_week).where("games.time < ?", Time.now)
    # results = picks.group(:result).count
    colors = []
    res_colors = {"win" => "green", "loss" => "red", "no result" => "blue"}
    # results.each do |res, count|
    #   results_hash = {}
    # weekly_distro = picks.where(:result => res)
    weekly_distro = picks.group(:game_id, :winner_id).count.sort_by {|k, v| v}.reverse.to_h
    weekly_distro.each do |key, pick_count|
      pick = Pick.find_by(:winner_id => key[1])
      winning_team = Team.find(key[1]).name
      game = Game.find(key[0])
      res = pick.result

      if game.home_team_id == pick.winner_id
        spread = game.home_spread
      else
        spread = game.home_spread * -1
      end
      if spread > 0
        spread = "+#{spread}"
      end
      labels = "#{winning_team} (#{spread})"
      # results_hash[labels] = pick_count
      if res == nil
        res = 'no result'
      end
      colors << res_colors[res]
      distribution_hash[winning_team] = pick_count
    end
    render json: [{name: "Number of Picks", data: distribution_hash, colors: colors}]
  end
end
