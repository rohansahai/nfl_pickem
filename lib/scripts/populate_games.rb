require 'open-uri'
Rails.application.eager_load!
url = "http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Football&sportsubtype=nfl"

team_names = Team.all.map { |team| team.name }

doc = Nokogiri::Slop(open(url))
nodes = doc.xpath("//event")
nodes.each do |node|
  game_data = {}
  game_data[:time] = node.event_datetimegmt.children.text
  game_data[:week] = 11

  begin
    if defined? node.periods.period.length
      game_data[:home_spread] = node.periods.period.first.spread.spread_home.text
    else
      game_data[:home_spread] = node.periods.period.spread.spread_home.text
    end
  rescue Exception => e
    puts "unable to pull spread for game with following data:"
    puts "#{node.participants.participant[0].participant_name.text} vs #{node.participants.participant[1].participant_name.text}"
    next
  end

  node.participants.participant.each do |team|
    if team.participant_name.text.include?("(n)")
      puts team.participant_name.text
      puts "LONDON"
      team_name = 'Oakland Raiders'
    else
    # if team.participant_name.text == 'Cincinnati Bengals (n)'
    #   team_name = 'Cincinnati Bengals'
    # else
    #   team_name = team.participant_name.text
    # end
      team_name = team.participant_name.text
    end

    next if !team_names.include? team_name

    if (team.visiting_home_draw.text == 'Home')
      game_data[:home_team_id] = Team.find_by(:name => team_name).id
    else
      game_data[:away_team_id] = Team.find_by(:name => team_name).id
    end
  end

  game = Game.find_by(game_data)
  Game.create(game_data) unless game
end

puts 'done'