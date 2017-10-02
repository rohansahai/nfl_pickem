class User < ApplicationRecord
  has_many :picks, dependent: :destroy

  def self.from_omniauth(auth)
    where(provider: auth.provider, uid: auth.uid).first_or_initialize.tap do |user|
      user.provider = auth.provider
      user.uid = auth.uid
      user.name = auth.info.name
      user.email = auth.info.email
      user.oauth_token = auth.credentials.token
      user.oauth_expires_at = Time.at(auth.credentials.expires_at)
      user.save!
    end
  end

  def self.send_initial_picks_texts
    url = "http://ancient-wildwood-19051.herokuapp.com/picks"
    body = "Spreads are in! Pick here - #{url} ."
    User.all.each {|user| user.send_text(body)}
  end

  def self.send_picks_reminder_texts
    url = "http://ancient-wildwood-19051.herokuapp.com/picks"
    week = Game.get_week
    User.all.each do |user|
      picks = user.picks.where(:week => week)
      if picks.count < 5
        body = "You've made #{picks.count}/5 picks for this week. Get your picks in here: #{url} ."
      end
      user.send_text(body)
    end
  end

  def wins
    picks.where(:result => 'win').count
  end

  def losses
    picks.where(:result => 'loss').count
  end

  def pushes
    picks.where(:result => 'push').count
  end

  def points
    wins + (pushes * 0.5)
  end

  def percent
    total = wins + losses + pushes
    if total > 0
      perc = (wins + (pushes * 0.5))  / total * 100
      perc.round()
    else
      return 0
    end
  end

  def week_standings
    week = Game.get_week
    week_standings = Hash.new
    week.downto(1).each do |this_week|
      week_wins = picks.where(:result => 'win', :week => this_week).count
      week_pushes = picks.where(:result => 'push', :week => this_week).count
      week_losses = picks.where(:result => 'loss', :week => this_week).count
      week_points = week_wins + (week_pushes * 0.5)
      total = week_wins + week_losses + week_pushes
      percent = total > 0 ? (week_points  / total * 100).round : 0

      week_standings[this_week] = {
        :wins => week_wins,
        :pushes => week_pushes,
        :losses => week_losses,
        :points => week_points,
        :percent => percent
      }
    end

    percentage_all = (points / picks.count) * 100
    week_standings[:all] = {wins: wins, pushes: pushes, points: points, percent: percentage_all.round}
    week_standings
  end

  def get_picks_summary(week)
    weekly_picks = picks.where(:week => week)
    if weekly_picks.count < 1
      "You haven't made any picks yet for week #{week}. Text space separated team names to make picks for this week."
    else
      text = "You're current picks for this week are: \n"
      weekly_picks.each do |pick|
        spread = pick.game.get_spread_pretty(pick.winner.id)


        text += "#{pick.winner.name} #{spread} #{pick.location} vs the #{pick.opponent.name}\n"
      end

      picks_remaining = 5 - weekly_picks.count
      text += "\n You have #{picks_remaining} picks remaining"
    end
  end

  def send_text(body)
    begin
      twilio_client = Twilio::REST::Client.new ENV['TWILIO_SID'], ENV['TWILIO_AUTH_TOKEN']
      twilio_client.messages.create(
        from: ENV['TWILIO_PHONE_NUMBER'],
        to: phone_number,
        body: body
      )
    rescue Twilio::REST::RequestError => e
      logger.error("Error sending twilio message to user #{name}")
    end
  end
end
