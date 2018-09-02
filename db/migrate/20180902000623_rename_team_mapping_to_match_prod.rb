class RenameTeamMappingToMatchProd < ActiveRecord::Migration[5.0]
  def change
    # someone changed this in prod, no idea why, just updating the table name on dev
    # to not break any scripts
    rename_table :team_mappings, :team_mapping
  end
end
