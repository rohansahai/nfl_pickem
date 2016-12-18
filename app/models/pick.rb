class Pick < ApplicationRecord
  include ActiveModel::Dirty

  belongs_to :user
  belongs_to :game
  belongs_to :winner, class_name: "Team"

  validate :pick_locked, :on => [:create, :update, :destroy]
  validate :max_picks, :on => :create
  validates :game_id, uniqueness: { scope: :user_id,
    message: "should only exist once per user" }

  MAX_PICKS = 5

  def self.update_pick_results_from_game_results(week)
    Game.where(:week => week).each do |game|
      game.picks.where(:result => nil).each do |pick|
        if game.push
          pick.update(:result => 'push')
        elsif pick.winner_id == game.spread_winner_id
          pick.update(:result => 'win')
        else
          pick.update(:result => 'loss')
        end
      end
    end
  end

  def self.parse_mobile_picks(user, week, text_body)
    picks = []
    teams = Team.get_teams_from_text text_body
    teams.each do |team|
      game = Game.find_by_team_and_week(team, week)
      raise "Game with team #{team.name} not found for week #{week}" if game.nil?

      pick = user.picks.create({
        :game_id => game.id,
        :winner_id => team.id,
        :week => week
      })

      raise "Pick with #{team.name} is invalid: #{pick.errors}" if !pick.valid?
      picks.push pick
    end

    picks
  end

  def opponent
    (game.home_team_id == winner.id) ? game.away_team : game.home_team
  end

  def location
    (game.home_team_id == winner.id) ? "HOME" : "AWAY"
  end

  private

  def max_picks
    if self.user.picks.where(:week => week).length + 1 > MAX_PICKS
      errors.add(:pick, "Already reached 5 picks")
    end
  end

  def pick_locked
    # allow updates on result
    return true if self.result_changed? && !self.winner_id_changed?

    if self.game.time < Time.now
      errors.add(:pick, "Game has already started")
    end
  end
end
