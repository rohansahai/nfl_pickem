class AlterGamesChangeSpreadColumnType < ActiveRecord::Migration[5.0]
  def change
    change_column :games, :home_spread, :decimal, precision: 3, scale: 1
  end
end
