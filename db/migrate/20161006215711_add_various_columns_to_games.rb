class AddVariousColumnsToGames < ActiveRecord::Migration[5.0]
  def change
    remove_column :games, :result
    rename_column :games, :spread, :home_spread
    add_column :games, :spread_winner_id, :integer, foreign_key: true, index: true
    add_column :games, :moneyline_winner_id, :integer, foreign_key: true, index: true
    add_column :games, :push, :boolean
    add_column :games, :home_team_score, :integer
    add_column :games, :away_team_score, :integer
    add_column :games, :game_status, :string
    add_column :games, :wins, :integer
    add_column :games, :losses, :integer
  end
end
