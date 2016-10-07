require 'csv'
Rails.application.eager_load!
ActiveRecord::Base.transaction do
  CSV.foreach("existing_picks_website-Table 1.csv") do |row|
    next if row[0] == 'user_id'
    # find game
    game = Game.find_by("(home_team_id = ? or away_team_id = ?) and week = ?", row[2], row[2], row[4])
    Pick.create([:week => row[4], :winner_id => row[1], :user_id => row[0], :game_id => game.id])
    # if (game.spread_winner_id.nil? || game.moneyline_winner_id.nil?)
    #   game.update(:spread_winner_id => row[3], :moneyline_winner_id => row[2])
    # end
  end
end
