$overlay = $('.overlay-text');

google.setOnLoadCallback(drawChart);
google.load("visualization", "1", {packages:["motionchart"]});

function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Player');
  data.addColumn('number', 'Year');
  data.addColumn('number', 'X pos');
  data.addColumn('number', 'Y pos');
  data.addColumn('string', 'Team');
  data.addColumn('number', 'poop');
  $.getJSON("GSWvsCLE.json", function(rawData) {
    console.log(rawData);
    var chartData = [];

    var firstEventMoments = rawData['events'][1]['moments'];
    // Loop through each moment
    for (var i=0;i<firstEventMoments.length;i++) {
      // Get the positions of every player
      positionsArray = firstEventMoments[i][5];

      chartTime = i + 100;

      chartData.push(['Ball', chartTime, positionsArray[0][2], positionsArray[0][3], 'Ball', 1]);
      chartData.push(['James', chartTime, positionsArray[1][2], positionsArray[1][3], 'CLE', 10]);
      chartData.push(['Smith', chartTime, positionsArray[2][2], positionsArray[2][3], 'CLE', 100]);
      chartData.push(['Love', chartTime, positionsArray[3][2], positionsArray[3][3], 'CLE', 15]);
      chartData.push(['Irving', chartTime, positionsArray[4][2], positionsArray[4][3], 'CLE', 50]);
      chartData.push(['Mozgov', chartTime, positionsArray[5][2], positionsArray[5][3], 'CLE', 23]);
      chartData.push(['Bogut', chartTime, positionsArray[6][2], positionsArray[6][3], 'GSW', 70]);
      chartData.push(['Curry', chartTime, positionsArray[7][2], positionsArray[7][3], 'GSW', 230]);
      chartData.push(['Thompson', chartTime, positionsArray[8][2], positionsArray[8][3], 'GSW', 17]);
      chartData.push(['Green', chartTime, positionsArray[9][2], positionsArray[9][3], 'GSW', 90]);
      chartData.push(['Barnes', chartTime, positionsArray[10][2], positionsArray[10][3], 'GSW', 150]);
    }
    // console.log(chartData);
    data.addRows(chartData);
    var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));

    var options = {};
    options['state'] = '{"nonSelectedAlpha":1,"xZoomedDataMin":2.04248,"iconType":"BUBBLE","yAxisOption":"3","xLambda":1,"orderedByY":false,"playDuration":6327.777777777781,"duration":{"multiplier":1,"timeUnit":"Y"},"yZoomedDataMax":45.4898,"yZoomedDataMin":3.37126,"xZoomedIn":false,"uniColorForNonSelected":false,"time":"0100","yZoomedIn":false,"yLambda":1,"showTrails":false,"dimensions":{"iconDimensions":["dim0"]},"xZoomedDataMax":73.22737,"iconKeySettings":[{"key":{"dim0":"Bogut"}},{"key":{"dim0":"Smith"}},{"key":{"dim0":"Barnes"}},{"key":{"dim0":"Green"}},{"key":{"dim0":"Thompson"}},{"key":{"dim0":"James"}},{"key":{"dim0":"Mozgov"}},{"key":{"dim0":"Curry"}},{"key":{"dim0":"Love"}},{"key":{"dim0":"Irving"}}],"xAxisOption":"2","colorOption":"4","orderedByX":false,"sizeOption":"_UNISIZE"}';
    options['width'] = 1000;
    options['height'] = 500;
    options['backgroundColor'] = 'transparent';
    options['showChartButtons'] = false;
    options['showXMetricPicker'] = false;
    options['showYMetricPicker'] = false;
    options['showXScalePicker'] = false;
    options['showyScalePicker'] = false;

    function placeMarker(dataTable) {
      console.log('placemarker called');

      // var cli = this.getChartLayoutInterface();
      // var chartArea = cli.getChartAreaBoundingBox();

      // console.log(dataTable.getValue(0, 3));
      // "Zombies" is element #5.
      // document.querySelector('.overlay-marker').style.top = Math.floor(cli.getYLocation(dataTable.getValue(0, 3))) - 50 + "px";
      // document.querySelector('.overlay-marker').style.left = Math.floor(cli.getXLocation(dataTable.getValue(0, 2))) - 10 + "px";
      // document.querySelector('.overlay-marker').style.top = "100px";
      // document.querySelector('.overlay-marker').style.left = "15px";

      // Check every 100 ms what time step the chart is at and update the overlay text
      window.setInterval(function(){
        var currentTime = JSON.parse(this.getState()).time;
        currentTime = currentTime.slice(0,4);
        $overlay.text("Time: "+currentTime);
      }.bind(this), 100);
    }

    // function onStateChange(dataTable) {
    //   console.log('state changed!');
    //   console.log(this.getState());
    // }

    google.visualization.events.addListener(chart, 'ready', placeMarker.bind(chart, data));
    // google.visualization.events.addListener(chart, 'statechange', onStateChange.bind(chart, data));
    chart.draw(data, options);
  });

}