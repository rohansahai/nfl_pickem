# rake db:data:dump RAILS_ENV=production
# rake db:data:load <-- NEVER RUN THIS ONE WITH PRODUCTION SET

# ids = User.select(:id)
# Pick.where.not(user_id: ids).delete_all

# Pick.where("created_at < ?", Time.new(2019, 06, 01)).update_all(league_id: 1)