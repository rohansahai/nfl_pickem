desc "This task is called by the Heroku scheduler add-on"

task :update_results => :production do
  puts "Updating game results..."
  Game.get_game_results_and_update_picks()
end