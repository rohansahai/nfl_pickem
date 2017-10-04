class AddLogoPathToTeams < ActiveRecord::Migration[5.0]
  def change
    add_column :games, :logo_path, :string
  end
end
