class WeeksController < ApplicationController
  def index
    # @picks = Pick.all
    @current_week = current_week
    respond_to do |format|
      format.html
    end
  end
end
