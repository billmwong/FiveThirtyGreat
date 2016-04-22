// // Load the Visualization API and the corechart package.
// google.charts.load('current', {'packages':['corechart']});

// // Set a callback to run when the Google Visualization API is loaded.
// google.charts.setOnLoadCallback(drawChart);

// // Callback that creates and populates a data table,
// // instantiates the pie chart, passes in the data and
// // draws it.
// function drawChart() {

//   // Create the data table.
//   var data = new google.visualization.DataTable();
//   data.addColumn('string', 'Topping');
//   data.addColumn('number', 'Slices');
//   data.addRows([
//     ['Mushrooms', 3],
//     ['Onions', 1],
//     ['Olives', 1],
//     ['Zucchini', 1],
//     ['Pepperoni', 2]
//   ]);

//   // Set chart options
//   var options = {'title':'How Much Pizza I Ate Last Night',
//                  'width':400,
//                  'height':300};

//   // Instantiate and draw our chart, passing in some options.
//   var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
//   chart.draw(data, options);
// }

google.load("visualization", "1", {packages:["motionchart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Player');
  data.addColumn('number', 'Year');
  data.addColumn('number', 'X pos');
  data.addColumn('number', 'Y pos');
  data.addColumn('string', 'Team');
  data.addRows([
    ['Steph',  1, 1000, 300, 'GSW'],
    ['Irving', 1, 1150, 200, 'CLE'],
    ['Ball', 1, 300,  250, 'ball'],
    ['Steph',  2, 1200, 400, 'GSW'],
    ['Irving', 2, 750,  150, 'CLE'],
    ['Ball', 2, 788,  617, 'ball']
  ]);

  var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));

  chart.draw(data, {width: 600, height:300});
}