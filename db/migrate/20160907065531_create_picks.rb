class CreatePicks < ActiveRecord::Migration[5.0]
  def change
    create_table :picks do |t|
      t.integer :user_id, index: true, foreign_key: true, null: false
      t.integer :game_id, index: true, foreign_key: true, null: false
      t.integer :winner_id, index: true, foreign_key: true, null: false
      t.integer :week, null: false
      t.boolean :win

      t.timestamps
    end
  end
end
