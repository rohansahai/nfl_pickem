class CleanUpDataForLeagues < ActiveRecord::Migration[5.0]
  def up
    ids = User.select(:id)
    Pick.where.not(user_id: ids).delete_all
    Pick.where("created_at < ?", Time.new(2019, 06, 01)).update_all(league_id: 1)
    change_column :picks, :league_id, :integer, null: false
  end

  def down
    change_column :picks, :league_id, :integer, null: false
  end
end
