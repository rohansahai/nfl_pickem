OmniAuth.config.logger = Rails.logger
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE if Rails.env.development?
Rails.application.config.middleware.use OmniAuth::Builder do
  provider :google_oauth2,
  ENV['GOOGLE_CLIENT_ID'],
  ENV['GOOGLE_CLIENT_SECRET'],
  :client_options => { :ssl => { :verify => !Rails.env.development? } }
end
