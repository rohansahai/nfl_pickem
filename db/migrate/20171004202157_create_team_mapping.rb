class CreateTeamMapping < ActiveRecord::Migration[5.0]
  def change
    create_table :team_mappings do |t|
      t.string :name
      t.string :short_name
      t.string :last_name
      t.string :team_abr

      t.timestamps
    end
  end
end
