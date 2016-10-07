require 'open-uri'
url = "http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Football&sportsubtype=nfl"

team_names = Team.all.map { |team| team.name }

doc = Nokogiri::Slop(open(url))
nodes = doc.xpath("//event")
nodes.each do |node|
  game_data = {}
  game_data[:time] = node.event_datetimegmt.children.text
  game_data[:week] = 5

  begin
    if defined? node.periods.period.length
      game_data[:spread] = node.periods.period.first.spread.spread_home.text
    else
      game_data[:spread] = node.periods.period.spread.spread_home.text
    end
  rescue Exception => e
    puts "unable to pull spread for game with following data:"
    puts "#{node.participants.participant[0].participant_name.text} vs #{node.participants.participant[1].participant_name.text}"
    next
  end

  node.participants.participant.each do |team|
    next if !team_names.include? team.participant_name.text

    if (team.visiting_home_draw.text == 'Home')
      game_data[:home_team_id] = Team.find_by(:name => team.participant_name.text).id
    else
      game_data[:away_team_id] = Team.find_by(:name => team.participant_name.text).id
    end
  end

  game = Game.find_by(game_data)
  Game.create(game_data) unless game
end

puts 'done'