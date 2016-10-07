require 'csv'
ActiveRecord::Base.transaction do
  CSV.foreach("existing_picks_website-Table 1.csv") do |row|
    next if row[0] == 'user_id'
    begin
      # find game
      game = Game.find_by("(home_team_id = ? or away_team_id = ?) and week = ?", row[2], row[2], row[4])
      if (game.spread_winner_id.nil? || game.moneyline_winner_id.nil?)
        game.update(:spread_winner_id => row[3], :moneyline_winner_id => row[2])
      end
    rescue Exception => e
      byebug
    end
  end
end
