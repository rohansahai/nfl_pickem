class ChartsController < ApplicationController
  def distribution
    distribution_hash = {}
    picks = Pick.joins(:game).where(:week => 1).where("games.time < ?", Time.now)
    results = picks.group(:result).count
    results.each do |res, count|
      results_hash = {}
      # weekly_distro = picks.where(:result => res)
      weekly_distro = picks.group(:game_id, :winner_id).where(:result => res).count.sort_by {|k, v| v}.reverse.to_h
      weekly_distro.each do |key, pick_count|
        pick = Pick.find_by(:winner_id => key[1])
        winning_team = Team.find(key[1]).name
        game = Game.find(key[0])
        if key[1] == game.spread_winner_id
          res = "win"
        elsif game.spread_winner_id == nil
          res = "no result"
        else
          res = "loss"
        end

        if game.home_team_id == pick.winner_id
          spread = game.home_spread
        else
          spread = game.home_spread * -1
        end
        if spread > 0
          spread = "+#{spread}"
        end
        labels = "#{winning_team} (#{spread})"
        results_hash[labels] = pick_count
        distribution_hash[res] = results_hash
      end
    end
    render json: [
      {name: "Win", data: distribution_hash["win"]},
      {name: "Loss", data: distribution_hash["loss"]},
      {name: "No Result", data: distribution_hash["no result"]}]
  end
end
