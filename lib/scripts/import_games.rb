require 'csv'
Rails.application.eager_load!
ActiveRecord::Base.transaction do
  CSV.foreach("games_table.csv") do |row|
    next if row[0] == 'week'
    game = Game.find_by(:week => row[0], :home_team_id => row[1], :away_team_id => row[2])
    game.update(:home_spread => row[3])
    # d = DateTime.strptime(row[4], "%m/%d/%Y %H:%M")
    # d.change(:offset => "-05:00")
    # Game.create(:week => row[0], :home_team_id => row[1], :away_team_id => row[2], :home_spread => row[3], :time => d)
  end
end