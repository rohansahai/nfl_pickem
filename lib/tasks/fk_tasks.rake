
desc 'dealing with fks while importing local data'

namespace :db do
    namespace :data do
        task :drop_fks do 
            ActiveRecord::Migration[5.0].remove_foreign_key :games, column: :home_team_id
            ActiveRecord::Migration[5.0].remove_foreign_key :games, column: :away_team_id
            ActiveRecord::Migration[5.0].remove_foreign_key :games, column: :spread_winner_id
            ActiveRecord::Migration[5.0].remove_foreign_key :games, column: :moneyline_winner_id
            ActiveRecord::Migration[5.0].remove_foreign_key :picks, :users
            ActiveRecord::Migration[5.0].remove_foreign_key :picks, :games
            ActiveRecord::Migration[5.0].remove_foreign_key :picks, column: :winner_id
            ActiveRecord::Migration[5.0].remove_foreign_key :picks, :leagues
            ActiveRecord::Migration[5.0].remove_foreign_key :leagues_users, :users
            ActiveRecord::Migration[5.0].remove_foreign_key :leagues_users, :leagues
            ActiveRecord::Migration[5.0].remove_foreign_key :leagues, column: :creator_id
        end

        task :add_fks do 
            ActiveRecord::Migration[5.0].add_foreign_key :games, :teams, column: :home_team_id
            ActiveRecord::Migration[5.0].add_foreign_key :games, :teams, column: :away_team_id
            ActiveRecord::Migration[5.0].add_foreign_key :games, :teams, column: :spread_winner_id
            ActiveRecord::Migration[5.0].add_foreign_key :games, :teams, column: :moneyline_winner_id
            ActiveRecord::Migration[5.0].add_foreign_key :picks, :users
            ActiveRecord::Migration[5.0].add_foreign_key :picks, :games
            ActiveRecord::Migration[5.0].add_foreign_key :picks, :teams, column: :winner_id
            ActiveRecord::Migration[5.0].add_foreign_key :picks, :leagues
            ActiveRecord::Migration[5.0].add_foreign_key :leagues_users, :users
            ActiveRecord::Migration[5.0].add_foreign_key :leagues_users, :leagues
            ActiveRecord::Migration[5.0].add_foreign_key :leagues, :users, column: :creator_id
        end
    end
end

# Run before db:data:load
Rake::Task["db:data:load"].enhance ["db:data:drop_fks"]

# Run after db:data:load
Rake::Task["db:data:load"].enhance do
    Rake::Task["db:data:add_fks"].invoke
end