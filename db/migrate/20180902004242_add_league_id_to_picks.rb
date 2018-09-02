class AddLeagueIdToPicks < ActiveRecord::Migration[5.0]
  def change
    add_column :picks, :league_id, :integer
    add_foreign_key :picks, :leagues
    add_index :picks, :league_id
  end
end
