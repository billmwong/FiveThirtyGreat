google.setOnLoadCallback(drawChart);
google.load("visualization", "1", {packages:["motionchart"]});

function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Player');
  data.addColumn('number', 'Year');
  data.addColumn('number', 'X pos');
  data.addColumn('number', 'Y pos');
  data.addColumn('string', 'Team');
  // data.addRows([
  //   ['Steph',  1, 1000, 300, 'GSW'],
  //   ['Irving', 1, 1150, 200, 'CLE'],
  //   ['Ball', 1, 300,  250, 'ball'],
  //   ['Steph',  2, 1200, 400, 'GSW'],
  //   ['Irving', 2, 750,  150, 'CLE'],
  //   ['Ball', 2, 788,  617, 'ball']
  // ]);
  $.getJSON("GSWvsCLE.json", function(rawData) {
    console.log(rawData);
    var chartData = [];

    var firstEventMoments = rawData['events'][0]['moments'];
    // Loop through each moment
    for (var i=0;i<firstEventMoments.length;i++) {
      // Get the positions of every player
      positionsArray = firstEventMoments[i][5];

      chartTime = i + 100;

      chartData.push(['Ball', chartTime, positionsArray[0][2], positionsArray[0][3], 'Ball']);
      chartData.push(['James', chartTime, positionsArray[1][2], positionsArray[1][3], 'CLE']);
      chartData.push(['Smith', chartTime, positionsArray[2][2], positionsArray[2][3], 'CLE']);
      chartData.push(['Love', chartTime, positionsArray[3][2], positionsArray[3][3], 'CLE']);
      chartData.push(['Irving', chartTime, positionsArray[4][2], positionsArray[4][3], 'CLE']);
      chartData.push(['Mozgov', chartTime, positionsArray[5][2], positionsArray[5][3], 'CLE']);
      chartData.push(['Bogut', chartTime, positionsArray[6][2], positionsArray[6][3], 'GSW']);
      chartData.push(['Curry', chartTime, positionsArray[7][2], positionsArray[7][3], 'GSW']);
      chartData.push(['Thompson', chartTime, positionsArray[8][2], positionsArray[8][3], 'GSW']);
      chartData.push(['Green', chartTime, positionsArray[9][2], positionsArray[9][3], 'GSW']);
      chartData.push(['Barnes', chartTime, positionsArray[10][2], positionsArray[10][3], 'GSW']);
    }
    // console.log(chartData);
    data.addRows(chartData);
    var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));

    var options = {};
    options['state'] = '{"yZoomedIn":false,"iconKeySettings":[{"key":{"dim0":"Mozgov"}},{"key":{"dim0":"Ball"}},{"key":{"dim0":"Barnes"}},{"key":{"dim0":"Smith"}},{"key":{"dim0":"Bogut"}},{"key":{"dim0":"Irving"}},{"key":{"dim0":"Love"}},{"key":{"dim0":"Curry"}},{"key":{"dim0":"James"}},{"key":{"dim0":"Thompson"}},{"key":{"dim0":"Green"}}],"showTrails":false,"uniColorForNonSelected":false,"duration":{"multiplier":1,"timeUnit":"Y"},"yLambda":1,"yZoomedDataMax":45.4898,"yZoomedDataMin":3.37126,"dimensions":{"iconDimensions":["dim0"]},"nonSelectedAlpha":0.4,"time":"0100","orderedByY":false,"xAxisOption":"2","colorOption":"4","playDuration":6327.777777777781,"sizeOption":"_UNISIZE","orderedByX":false,"xLambda":1,"xZoomedDataMin":2.04248,"iconType":"BUBBLE","xZoomedIn":false,"yAxisOption":"3","xZoomedDataMax":73.22737}';
    options['width'] = 1000;
    options['height'] = 600;
    // options['backgroundColor'] = 'transparent';
    options['showChartButtons'] = false;
    options['showXMetricPicker'] = false;
    options['showYMetricPicker'] = false;
    options['showXScalePicker'] = false;
    options['showyScalePicker'] = false;
    // backgroundColor: "transparent"


    function placeMarker(dataTable) {
      var cli = this.getChartLayoutInterface();
      var chartArea = cli.getChartAreaBoundingBox();

      console.log(dataTable.getValue(0, 3));
      // "Zombies" is element #5.
      document.querySelector('.overlay-marker').style.top = Math.floor(cli.getYLocation(dataTable.getValue(0, 3))) - 50 + "px";
      document.querySelector('.overlay-marker').style.left = Math.floor(cli.getXLocation(dataTable.getValue(0, 2))) - 10 + "px";
    }

    // var chart = new google.visualization.LineChart(document.getElementById('line-chart-marker'));
    google.visualization.events.addListener(chart, 'ready', placeMarker.bind(chart, data));
    chart.draw(data, options);
  });

}
