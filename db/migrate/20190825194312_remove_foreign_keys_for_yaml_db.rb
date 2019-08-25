class RemoveForeignKeysForYamlDb < ActiveRecord::Migration[5.0]
  def up
    if Rails.env.development?
      remove_foreign_key :games, column: :home_team_id
      remove_foreign_key :games, column: :away_team_id
      remove_foreign_key :games, column: :spread_winner_id
      remove_foreign_key :games, column: :moneyline_winner_id
      remove_foreign_key :picks, :users
      remove_foreign_key :picks, :games
      remove_foreign_key :picks, column: :winner_id
      remove_foreign_key :picks, :leagues
      remove_foreign_key :leagues_users, :users
      remove_foreign_key :leagues_users, :leagues
    end
  end

  def down
    if Rails.env.development?
      add_foreign_key :games, :teams, column: :home_team_id
      add_foreign_key :games, :teams, column: :away_team_id
      add_foreign_key :games, :teams, column: :spread_winner_id
      add_foreign_key :games, :teams, column: :moneyline_winner_id

      add_foreign_key :picks, :users
      add_foreign_key :picks, :games
      add_foreign_key :picks, :leagues
      add_foreign_key :picks, :teams, column: :winner_id

      add_foreign_key :leagues_users, :users
      add_foreign_key :leagues_users, :leagues
    end
  end
end
