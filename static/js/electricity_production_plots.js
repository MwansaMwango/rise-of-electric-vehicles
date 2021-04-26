/* global Plotly */
var country = "SE";
var source = ['Oil, gas and coal', 'Renewable sources, excluding hydroelectric', 'Nuclear', 'Natural Gas', 'Hydroelectric'];
var year1 = []; var year2 = []; var year3 = []; var year4 = []; var year5 = [];
var percentages1 = []; percentages2 = []; percentages3 = []; percentages4 = []; percentages5 = [];

var url =
  `http://localhost:5000/api/v1/resources/electricity_production_values/country?id=${country}`;


function buildPlot() {
  d3.json(url).then(function(data) {

    var country = data[0].country;
            
    // Grab values from the data json object to build the plots
    for (var i = 0; i < data.length; i++) {
      
      switch(data[i].source_id) {
        case "EG.ELC.FOSL.ZS":
          percentages1.push(data[i].percentage)
          year1.push(data[i].year);
          break;
        case "EG.ELC.RNWX.ZS":
          percentages2.push(data[i].percentage)
          year2.push(data[i].year);
          break;
        case "EG.ELC.NUCL.ZS":
          percentages3.push(data[i].percentage)
          year3.push(data[i].year);
          break;
        case "EG.ELC.NGAS.ZS":
          percentages4.push(data[i].percentage)
          year4.push(data[i].year);
          break;
        case "EG.ELC.HYRO.ZS":
          percentages5.push(data[i].percentage)
          year5.push(data[i].year);
          break;
        default:
          var message = "Unknown";
      }
      
    }

    console.log("here");

    var trace1 = {
      mode: "lines",
      name: source[0],
      x: year1,
      y: percentages1,
      line: {
        color: "#17BECF"
      }
    };

    var trace2 = {
      mode: "lines",
      name: source[1],
      x: year2,
      y: percentages2,
    };

    var trace3 = {
      mode: "lines",
      name: source[2],
      x: year3,
      y: percentages3,
    };

    var trace4 = {
      mode: "lines",
      name: source[3],
      x: year4,
      y: percentages4,
    };

    var trace5 = {
      mode: "lines",
      name: source[4],
      x: year5,
      y: percentages5,
    };

    var datatr = [trace1, trace2, trace3, trace4, trace5];

    var layout = {
      title: `${country} - Electricity Generation by Source (% of total)`,
      xaxis: {
        title: 'Year'
      },
      yaxis: {
        autorange: true,
        type: "linear",
        title: 'Percentage'
      }
    };

    Plotly.newPlot("plot", datatr, layout);

  });
}

buildPlot();
