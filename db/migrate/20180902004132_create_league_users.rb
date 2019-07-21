class CreateLeagueUsers < ActiveRecord::Migration[5.0]
  def change
    create_table :league_users do |t|
      t.integer :user_id, index: true, foreign_key: true, null: false
      t.integer :league_id, index: true, foreign_key: true, null: false

      t.timestamps
    end
  end
end
