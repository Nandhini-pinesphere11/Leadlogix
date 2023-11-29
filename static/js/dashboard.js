(function($) {
  'use strict';
  $(function() {
    
    if ($("#north-america-chart").length) {
      // Make an AJAX request to your Django view
      $.ajax({
        url: '/get_customer_confidence_data/', 
        method: 'GET',
        dataType: 'json',
        success: function(data) {
          // Use the data obtained from the view to populate the chart
          var areaData = {
            labels: data.labels,  // Use the labels from the view's response
            datasets: [{
              data: data.values,  // Use the values from the view's response
              backgroundColor: [
                "#4B49AC","#FFC100", "#248AFD",
              ],
              borderColor: "rgba(0,0,0,0)"
            }]
          };

          var areaOptions = {
            responsive: true,
        maintainAspectRatio: true,
        segmentShowStroke: false,
        cutoutPercentage: 78,
        elements: {
          arc: {
              borderWidth: 4
          }
        },      
        legend: {
          display: false
        },
        tooltips: {
          enabled: true
        },
        legendCallback: function(chart) {
          var text = [];
          for (var i = 0; i < chart.data.datasets[0].data.length; i++) {
            text.push('<div class="d-flex justify-content-between mx-4 mx-xl-5 mt-3"><div class="d-flex align-items-center"><div class="mr-3" style="width:20px; height:20px; border-radius: 50%; background-color: ' + chart.data.datasets[0].backgroundColor[i] + '"></div><p class="mb-0">' + chart.data.labels[i] + '</p></div>');
            text.push('</div>');
          }
          return '<div class="report-chart">' + text.join("") + '</div>';
        },
          };

          var total_count = data.total_count;

          var northAmericaChartPlugins = {
            beforeDraw: function(chart) {
              var width = chart.chart.width,
                  height = chart.chart.height,
                  ctx = chart.chart.ctx;
          
              ctx.restore();
              var fontSize = 3.125;
              ctx.font = "500 " + fontSize + "em sans-serif";
              ctx.textBaseline = "middle";
              ctx.fillStyle = "#13381B";
          
              var text = total_count,
                  textX = Math.round((width - ctx.measureText(text).width) / 2),
                  textY = height / 2;
          
              ctx.fillText(text, textX, textY);
              ctx.save();
            }
          }

          // Render the chart
          var northAmericaChartCanvas = $("#north-america-chart").get(0).getContext("2d");
          var northAmericaChart = new Chart(northAmericaChartCanvas, {
            type: 'doughnut',
            data: areaData,
            options: areaOptions,
            plugins: northAmericaChartPlugins
          });

          northAmericaChart.canvas.onclick = function(evt) {
            var activeSlice = northAmericaChart.getElementAtEvent(evt)[0];
            if (activeSlice) {
              var selectedData = activeSlice._model.label;  // Extract the label of the clicked slice
              var url = '/manageforms/?selected_data=' + selectedData;
              window.open(url, '_blank'); // Redirect to manageforms page with selected_data query parameter
            }
          };

          // Render the legend
          document.getElementById('north-america-legend').innerHTML = northAmericaChart.generateLegend();
        },
        error: function(error) {
          console.error(error);
        }
      });
    } 
  });
})(jQuery);

(function($) {
  'use strict';
  $(function() {
    if ($("#sales-chart").length) {
    $.ajax({
        url: '/get_contact_count/',  // URL of the Django view
        type: 'GET',
        success: function(data) {
            var labels = data.map(function(item) {
              return moment(item.date).format('DD MMM').toUpperCase();
            });
            var counts = data.map(function(item) {
                return item.count;
            });

            var maxCount = Math.max(...counts); // Find the maximum count value
            var stepSize = Math.ceil(maxCount / 10); // Calculate the step size

            var SalesChartCanvas = $("#sales-chart").get(0).getContext("2d");
            var SalesChart = new Chart(SalesChartCanvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Count',
                        data: counts,
                        backgroundColor: '#98BDFF'
                    }]
                },
                options: {
                  cornerRadius: 5,
                  responsive: true,
                  maintainAspectRatio: true,
                  layout: {
                    padding: {
                      left: 0,
                      right: 0,
                      top: 20,
                      bottom: 0
                    }
                  },
                  scales: {
                    yAxes: [{
                      display: true,
                      gridLines: {
                        display: true,
                        drawBorder: false,
                        color: "#F2F2F2"
                      },
                      ticks: {
                        display: true,
                        min: 0,
                        max:  maxCount,
                        stepSize: stepSize, 
                        callback: function(value, index, values) {
                          return  value ;
                        },
                        autoSkip: true,
                        maxTicksLimit: 10,
                        fontColor:"#6C7383"
                      }
                    }],
                    xAxes: [{
                      stacked: false,
                      ticks: {
                        beginAtZero: true,
                        fontColor: "#6C7383"
                      },
                      gridLines: {
                        color: "rgba(0, 0, 0, 0)",
                        display: false
                      },
                      barPercentage: 1
                    }]
                  },
                  legend: {
                    display: false
                  },
                  elements: {
                    point: {
                      radius: 0
                    }
                  },
                  onClick: function(e, elements) {
                    if (elements.length > 0) {
                      var clickedDate = labels[elements[0]._index];
                      var formattedDate = moment(clickedDate, 'DD MMM').format('DD MM YYYY').split(' ').join('%20');
                      var url = '/manageforms/?selected_date=' + formattedDate;
                      window.open(url, '_blank');
                  }
                }
                },
            });
        }
    });
    document.getElementById('sales-legend').innerHTML = SalesChart.generateLegend();
  }
}); 
})(jQuery);