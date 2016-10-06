class Game < ApplicationRecord
  belongs_to :away_team, class_name: "Team"
  belongs_to :home_team, class_name: "Team"

  validates :week, uniqueness: { scope: :home_team_id,
    message: "should only exist once per week" }
  validates :week, uniqueness: { scope: :away_team_id,
    message: "should only exist once per week" }
end
