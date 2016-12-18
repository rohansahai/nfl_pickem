class Team < ApplicationRecord
  def self.get_teams_from_text(text_body)
    teams = []
    team_array = text_body.split(" ")
    team_array.each do |text|
      team = Team.find_by("name ILIKE ?", "%#{text}%")
      raise "Team: #{text} not found." if team.nil?
      teams.push team
    end

    teams
  end
end
