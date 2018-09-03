class AddMissingForeignKeys < ActiveRecord::Migration[5.0]
  def change
    add_foreign_key :games, :teams, column: :home_team_id
    add_foreign_key :games, :teams, column: :away_team_id
    add_foreign_key :games, :teams, column: :spread_winner_id
    add_foreign_key :games, :teams, column: :moneyline_winner_id

    add_foreign_key :picks, :users
    add_foreign_key :picks, :games
    add_foreign_key :picks, :teams, column: :winner_id

    add_foreign_key :leagues_users, :users
    add_foreign_key :leagues_users, :leagues
  end
end
