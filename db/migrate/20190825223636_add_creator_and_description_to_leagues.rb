class AddCreatorAndDescriptionToLeagues < ActiveRecord::Migration[5.0]
  def change
    add_column :leagues, :creator_id, :integer
    add_foreign_key :leagues, :users, column: :creator_id
    if Rails.env.development?
      remove_foreign_key :leagues, column: :creator_id
    end

    add_column :leagues, :description, :text
  end
end
