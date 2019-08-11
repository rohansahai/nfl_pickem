class RenameTeamMappingToMatchProd < ActiveRecord::Migration[5.0]
  def change
    # someone changed all this stuff directly in prod, fixing
    remove_column :team_mappings, :created_at, :datetime
    remove_column :team_mappings, :updated_at, :datetime
    rename_table :team_mappings, :team_mapping
    # add_column :teams, :logo_path, :string
    # add_column :teams, :wins, :integer
    # add_column :teams, :losses, :integer
  end
end
