class League < ApplicationRecord
  has_many :leagues_users
  has_many :users, through: :leagues_users
  has_many :picks
  belongs_to :creator, class_name: "User"
end
