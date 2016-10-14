Rails.application.routes.draw do
  get 'auth/:provider/callback', to: 'sessions#create'
  get 'auth/failure', to: redirect('/')
  get 'signout', to: 'sessions#destroy', as: 'signout'

  get 'picks', to: 'games#index'
  get 'standings', to: 'picks#standings'
  get 'previous', to: 'picks#index'
  get 'distribution', to: 'picks#distribution'

  resources :sessions, only: [:create, :destroy]
  resource :home, only: [:show]
  resources :weeks, only: [:index] do
    resources :games, only: [:index]
    resources :picks, only: [:create, :update, :destroy]
  end

  root to: redirect('/picks')
end
