module WeeksHelper
  def distribution
    # bar_chart Pick.joins(:winner).where(:week =>
    # @current_week).group(:name).count.sort_by {|k, v| v}.reverse.to_h,
    bar_chart distribution_charts_path, colors: ["green", "red", "blue", "gray"],
    height: '750px',
     library: {
      yAxis: {
         allowDecimals: false,
      },
#       plotOptions: {
#    bar: {
#       dataLabels: {
#           enabled: true,
#       }
#    }
# },
      tooltip: {
      pointFormat: 'Times Picked: <b>{point.y}</b>'}
    }
  end
end
