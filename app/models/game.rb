class Game < ApplicationRecord
  belongs_to :away_team, class_name: "Team"
  belongs_to :home_team, class_name: "Team"
  has_many :picks

  validates :week, uniqueness: { scope: :home_team_id,
    message: "should only exist once per week" }
  validates :week, uniqueness: { scope: :away_team_id,
    message: "should only exist once per week" }

  def self.get_game_results_and_update_picks()
    week = self.get_week
    ActiveRecord::Base.transaction do
      require 'csv'
      self.create_game_results_csv
      CSV.foreach("tmp/nfl_scores.csv") do |row|
        next if row[0] == 'away_team_id'
        away_team_id = row[0].to_i
        home_team_id = row[2].to_i
        next if row[5].to_i < week
        game = Game.find_by("(home_team_id = ? or away_team_id = ?) and week = ?", home_team_id, away_team_id, row[5])
        if (game && (game.spread_winner_id.nil? || game.moneyline_winner_id.nil?))
          away_team_score = row[1].to_i
          home_team_score = row[3].to_i

          winner_id, push = game.get_spread_winner(away_team_score, home_team_score, away_team_id, home_team_id)
          game.assign_attributes(
            :away_team_score => away_team_score,
            :home_team_score => home_team_score
          )

          # update only if game is over - this is hacky
          if ((Time.now - game.time)/60) > 240
            game.assign_attributes(
              :spread_winner_id => winner_id,
              :moneyline_winner_id => row[4].to_i,
              :push => push
            )
            game.save
            game.update_related_picks
          else
            game.save
          end

          puts "Updating #{home_team_id} vs #{away_team_id}"
        end
      end
    end
  end

  def self.get_week
    end_times = {
      11 => '2016-11-21',
      12 => '2016-11-28',
      13 => '2016-12-05',
      14 => '2016-12-12',
      15 => '2016-12-19',
      16 => '2016-12-26',
      17 => '2017-01-01'
    }

    active_week = false
    end_times.each do |week, end_date|
      if Date.today < Date.parse(end_date)
        active_week = week
        break
      end
    end

    active_week
  end

  def self.create_game_results_csv
    # this creates a csv at tmp/nfl_scores.csv
    `python3 lib/scripts/nfl_scores.py`
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
