var country = "Australia";

/* global Plotly */
var url =
  `http://localhost:5000/api/v1/resources/electricity_production_values/country?id=${country}`;

/**
 * Helper function to select data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - country
 * index 1 - index
 * index 2 - percentage
 * index 3 - source_id
 * index 4 - year
 */
function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

function buildPlot() {
  d3.json(url).then(function(data) {
    
    var example = ['test', 'test2']
    var country = data.country;
    var index = data.index;
    var percentage = data.percentage;
    var source_id = data.source_id;
    var year = data.year;
        
    // Grab values from the data json object to build the plots
    for (var i = 0; i < data.length; i++) {
      example.push(data[i].percentage)
    //   country.push(data[i].country);
    //   index.push(data[i].index);
    //   percentage.push(data[i].percentage);
    //   source_id.push(data[i].source_id);
    //   year.push(data[i].year);
    }

    console.log(example);

    // var trace1 = {
    //   type: "scatter",
    //   mode: "lines",
    //   name: name,
    //   x: dates,
    //   y: closingPrices,
    //   line: {
    //     color: "#17BECF"
    //   }
    // };

    // var data = [trace1];

    // var layout = {
    //   title: `${stock} closing prices`,
    //   xaxis: {
    //     range: [startDate, endDate],
    //     type: "date"
    //   },
    //   yaxis: {
    //     autorange: true,
    //     type: "linear"
    //   }
    // };

    // Plotly.newPlot("plot", data, layout);

  });
}

buildPlot();
