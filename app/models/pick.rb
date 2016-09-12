class Pick < ApplicationRecord
  belongs_to :user
  belongs_to :game
  belongs_to :winner, class_name: "Team"

  validate :pick_locked, :on => [:create, :update]
  validate :max_picks, :on => :create

  MAX_PICKS = 5

  private

  def max_picks
    if self.user.picks.length > MAX_PICKS
      errors.add(:pick, "Already reached 5 picks")
    end
  end

  def pick_locked
    if self.game.time < Time.now
      errors.add(:pick, "Game has already started")
    end
  end
end
