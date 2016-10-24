class User < ApplicationRecord
  has_many :picks, dependent: :destroy

  def self.from_omniauth(auth)
    where(provider: auth.provider, uid: auth.uid).first_or_initialize.tap do |user|
      user.provider = auth.provider
      user.uid = auth.uid
      user.name = auth.info.name
      user.oauth_token = auth.credentials.token
      user.oauth_expires_at = Time.at(auth.credentials.expires_at)
      user.save!
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
    (wins * 1) + (pushes * 0.5)
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
