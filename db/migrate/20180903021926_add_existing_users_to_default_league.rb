class AddExistingUsersToDefaultLeague < ActiveRecord::Migration[5.0]
  def up
    users = User.all.each do |user|
      LeaguesUser.find_or_create_by(user_id: user.id, league_id: 1)
    end
  end

  def down
    LeaguesUser.delete_all
  end
end
