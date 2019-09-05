class AddCreatorAndDescriptionToLeagues < ActiveRecord::Migration[5.0]
  def change
    add_column :leagues, :creator_id, :integer
    add_foreign_key :leagues, :users, column: :creator_id

    add_column :leagues, :description, :text
  end
end
