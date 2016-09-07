class CreateGames < ActiveRecord::Migration[5.0]
  def change
    create_table :games do |t|
      t.integer :week, null: false
      t.integer :home_team_id, index: true, foreign_key: true, null: false
      t.integer :away_team_id, index: true, foreign_key: true, null: false
      t.integer :spread, null: false

      t.timestamps
    end
  end
end
