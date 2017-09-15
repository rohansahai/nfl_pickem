module WeeksHelper
  def distribution
    # bar_chart Pick.joins(:winner).where(:week =>
    # @current_week).group(:name).count.sort_by {|k, v| v}.reverse.to_h,
    bar_chart distribution_charts_path,
     library: {
     color: "green",
      yAxis: {
         allowDecimals: false,
      },
      tooltip: {
      pointFormat: 'Times Picked: <b>{point.y}</b>'
    }
    }
  end
end
