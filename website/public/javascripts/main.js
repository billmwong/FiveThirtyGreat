TEAM_DICT = {
  'Ball':'Ball',
  'Curry': 'GSW',
  'Thompson': 'GSW',
  'Bogut': 'GSW',
  'Green': 'GSW',
  'Barnes': 'GSW',
  'James': 'CLE',
  'Smith': 'CLE',
  'Love': 'CLE',
  'Irving': 'CLE',
  'Mozgov': 'CLE',
  'pos': 'Possession'
};

console.log(START);

// var START = 3475;
// var END = 3835;
// var START = 5000;
// var END = 6000;
// var START = 4500;
// var END = 5000;

$overlay = $('.overlay-text');

google.setOnLoadCallback(drawChart);
google.load("visualization", "1", {packages:["motionchart"]});

function drawChart() {
  // Initialize the data columns
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Player');
  data.addColumn('number', 'Year');
  data.addColumn('number', 'X pos');
  data.addColumn('number', 'Y pos');
  data.addColumn('string', 'Team');
  data.addColumn('number', 'radius');

  // Load the json
  $.getJSON("dump.json", function(rawData) {
    console.log(rawData);
    var chartData = [];
    // Make a dummy ball size so that google charts scales the rest of the sizes correctly
    chartData.push(['Ball', (START+100), 0, 0, 'Ball', 150]);

    // var firstEventMoments = rawData['events'][1]['moments'];
    // Loop through each moment
    // for (var i=START;i<rawData['Ball'].length;i++) {
    for (var i=START;i<END;i++) {
      chartTime = i + 100;
      
      // Loop through each player, push the data for each
      for (var player in rawData) {
        // Make sure this key is not from prototype
        if (rawData.hasOwnProperty(player)) {
          // Only add the data if it's not pct, pos, or radius
          if (['pct','pos','radius'].indexOf(player) === -1) {
            // Default player radius
            var thisRadius = 15;
            if (player === 'Ball') {
              // This is the ball, so set its radius
              thisRadius = rawData['radius'][i];
            }
            chartData.push([
              player,
              chartTime,
              rawData[player][i][0],
              rawData[player][i][1],
              TEAM_DICT[player],
              thisRadius
            ]);
          }
        }
      }
    }
    data.addRows(chartData);
    var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));

    // Set the chart options
    var options = {};
    // options['state'] = '{"nonSelectedAlpha":1,"xZoomedDataMin":0,"iconType":"BUBBLE","yAxisOption":"3","xLambda":1,"orderedByY":false,"playDuration":6327.777777777781,"duration":{"multiplier":1,"timeUnit":"Y"},"yZoomedDataMax":50,"yZoomedDataMin":0,"xZoomedIn":false,"uniColorForNonSelected":false,"time":"0100","yZoomedIn":false,"yLambda":1,"showTrails":false,"dimensions":{"iconDimensions":["dim0"]},"xZoomedDataMax":94,"iconKeySettings":[{"key":{"dim0":"Bogut"}},{"key":{"dim0":"Smith"}},{"key":{"dim0":"Barnes"}},{"key":{"dim0":"Green"}},{"key":{"dim0":"Thompson"}},{"key":{"dim0":"James"}},{"key":{"dim0":"Mozgov"}},{"key":{"dim0":"Curry"}},{"key":{"dim0":"Love"}},{"key":{"dim0":"Irving"}}],"xAxisOption":"2","colorOption":"4","orderedByX":false,"sizeOption":"5"}';
    options['state'] = '{"yAxisOption":"3","orderedByX":false,"xZoomedDataMin":-5.29917,"iconType":"BUBBLE","xZoomedIn":false,"xLambda":1,"playDuration":40000,"duration":{"multiplier":1,"timeUnit":"Y"},"yZoomedDataMax":49.99803,"orderedByY":false,"showTrails":false,"uniColorForNonSelected":false,"time":"0100","yZoomedIn":false,"yLambda":1,"colorOption":"4","dimensions":{"iconDimensions":["dim0"]},"xZoomedDataMax":93.96206,"iconKeySettings":[{"key":{"dim0":"Ball"}}],"nonSelectedAlpha":1,"yZoomedDataMin":0,"xAxisOption":"2","sizeOption":"5"}';
    options['width'] = 1000;
    options['height'] = 500;
    options['backgroundColor'] = 'transparent';
    options['showChartButtons'] = false;
    options['showXMetricPicker'] = false;
    options['showYMetricPicker'] = false;
    options['showXScalePicker'] = false;
    options['showyScalePicker'] = false;

    function onChartReady(dataTable) {
      // Check every 100 ms what time step the chart is at and update the overlay text
      window.setInterval(function () {
        var rawTime = JSON.parse(this.getState()).time;
        // Get rid of the extra stuff if there's a dash
        if (rawTime.indexOf('-') > -1) {
          rawTime = rawTime.slice(0,rawTime.indexOf('-'));
        }
        var currentTime = parseInt(rawTime, 10);
        // Adjust for chart time
        var currentIndex = currentTime - 100;
        var rawPCT = rawData['pct'][currentIndex];
        var displayPCT = rawPCT.toString().slice(0,5);

        $overlay.text("PCT: " + displayPCT);
      }.bind(this), 100);
    }

    // Call onChartReady when the chart is ready
    google.visualization.events.addListener(chart, 'ready', onChartReady.bind(chart, data));

    // Draw the chart
    chart.draw(data, options);
  });

}