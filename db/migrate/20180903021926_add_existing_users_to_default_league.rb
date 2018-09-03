class AddExistingUsersToDefaultLeague < ActiveRecord::Migration[5.0]
  def up
    users = User.all.each do |user|
      LeaguesUser.first_or_create(user_id: user.id, league_id: 1)
    end
  end

  def down
    LeaguesUser.all.destroy
  end
end
