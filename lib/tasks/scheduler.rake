desc "This task is called by the Heroku scheduler add-on"

task :update_results => :environment do
  puts "Updating game results..."
  Game.update_scores_and_picks
  puts "Done."
end
