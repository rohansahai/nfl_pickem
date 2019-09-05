Rails.application.routes.draw do
  get 'auth/:provider/callback', to: 'sessions#create'
  get 'auth/failure', to: redirect('/')
  get 'signout', to: 'sessions#destroy', as: 'signout'

  get 'picks', to: 'games#index'
  get 'standings', to: 'picks#standings'
  get 'previous', to: 'picks#previous'
  # get 'distribution', to: 'picks#distribution'
  get 'users', to: 'users#index'
  get 'distribution', to: 'weeks#index'
  get 'change-league/:league_id', to: 'leagues#change_league'
  get 'league-invite/:league_id', to: 'leagues#league_invite'

  resources :sessions, only: [:create, :destroy]
  resources :leagues, only: [:index]
  resource :home, only: [:show]
  resources :weeks, only: [:index] do
    resources :games, only: [:index]
    resources :picks, only: [:create, :update, :destroy]
  end

  resources :charts, only: [] do
    collection do
      get 'distribution'
    end
  end

  resources :users, only: [] do
    resources :picks, only: :index
  end

  root to: redirect('/picks')
end
