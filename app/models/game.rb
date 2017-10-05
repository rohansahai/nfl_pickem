class Game < ApplicationRecord
  belongs_to :away_team, class_name: "Team"
  belongs_to :home_team, class_name: "Team"
  has_many :picks

  validates :week, uniqueness: { scope: :home_team_id,
    message: "should only exist once per week" }
  validates :week, uniqueness: { scope: :away_team_id,
    message: "should only exist once per week" }

  def self.get_game_results_and_update_picks()
    week = self.get_last_week_with_no_results
    week
  end

  def self.get_week
    end_times = {
      1 => '2017-09-13',
      2 => '2017-09-20',
      3 => '2017-09-27',
      4 => '2017-10-04',
      5 => '2017-10-11',
      6 => '2017-10-18',
      7 => '2017-10-25',
      8 => '2017-11-01',
      9 => '2017-11-08',
      10 => '2017-11-15',
      11 => '2017-11-22',
      12 => '2017-11-29',
      13 => '2017-12-06',
      14 => '2017-12-13',
      15 => '2017-12-20',
      16 => '2017-12-27',
      17 => '2018-01-03'
    }

    active_week = false
    end_times.each do |week, end_date|
      if Date.today < Date.parse(end_date)
        active_week = week
        break
      end
    end

    if active_week == false
      active_week = 17
    end

    active_week
  end

  def self.get_last_week_with_no_results
    last_week_with_no_results = self.get_week
    last_week = last_week_with_no_results - 1

    Game.where(:week => last_week).each do |game|
      if game.spread_winner_id.nil? && !game.push
        last_week_with_no_results = last_week
        break
      end
    end
    last_week_with_no_results
  end

  def self.update_scores_and_picks
    # this creates a csv at tmp/nfl_scores.csv
    `#{ENV['PYTHON_EXEC']} lib/scripts/nfl_scores.py`
  end

  def self.find_by_team_and_week(team, week)
    Game.find_by("home_team_id = ? OR away_team_id = ? AND week = ?", team.id, team.id, week)
  end

  def self.get_weekly_summary(week)
    games = Game.where(:week => week)
    text = "The spreads are in! Here is the breakdown for this week (home teams first): \n\n"
    games.each do |game|
      spread_pretty = game.get_spread_pretty(game.home_team_id)
      text += "#{game.home_team.name} #{spread_pretty} vs #{game.away_team.name}\n\n"
    end

    text+="\n\n Make your picks by replying to this text with space separated teams. I.E. 'jets panthers cardinals bills giants'"
  end

  def get_spread_winner(away_team_score, home_team_score, away_team_id, home_team_id)
    score_diff = away_team_score - home_team_score
    push = false

    if score_diff == home_spread
      push = true
    elsif score_diff < home_spread
      winner_id = home_team_id
    else
      winner_id = away_team_id
    end

    [winner_id, push]
  end

  def get_spread_pretty(winner_pick_id)
    if winner_pick_id == home_team_id
      spread_pretty = home_spread
    else
      spread_pretty = home_spread * -1
    end

    (spread_pretty > 0) ? "+#{spread_pretty}" : spread_pretty
  end

  def update_related_picks
    picks.where(:result => nil).each do |pick|
      if push
        pick.update(:result => 'push')
      elsif pick.winner_id == spread_winner_id
        pick.update(:result => 'win')
      else
        pick.update(:result => 'loss')
      end
    end
  end
end
