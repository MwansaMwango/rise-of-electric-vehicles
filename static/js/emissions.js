// Emissions data plotting

// Display the default plot
function init() {
  
  addCountryDropDown ();
  buildPlot("AU", "NO");

}

// Populate the country dropdown and default to Australia
function addCountryDropDown () {
 
  var url =
  `api/v1/resources/countries/all`;

  d3.json(url).then(function(data) {
    
    // add the entries to the first dropdown
    d3.select("#selDataset")
    .selectAll('myOptions')
    .data(d3.entries(data).map(function(d){return d}))
    .enter()
    .append('option')
    .text(function (d) { return d.value.Name; }) // text showed in the menu
    .attr("value", function (d) { return d.value.Code; }) // corresponding value returned by the button
    .property("selected", function(d){ return d.value.Name === "Australia"; })

    // add the entries to the second dropdown
    d3.select("#selDataset2")
    .selectAll('myOptions')
    .data(d3.entries(data).map(function(d){return d}))
    .enter()
    .append('option')
    .text(function (d) { return d.value.Name; }) // text showed in the menu
    .attr("value", function (d) { return d.value.Code; }) // corresponding value returned by the button
    .property("selected", function(d){ return d.value.Name === "Norway"; })
  });


}

// On change to the DOM, call functions
// 1st Country Dropdown
d3.selectAll("#selDataset").on("change", getData);
// 2nd Country Dropdown
d3.selectAll("#selDataset2").on("change", getData2);

// Functions called by DOM changes
function getData() {
  var dropdownMenu = d3.select("#selDataset");
  // Assign the value of the dropdown menu option to a variable
  var dataset = dropdownMenu.property("value");
  // console.log(dataset);
  updatePlot(dataset, 1);
}

function getData2() {
  var dropdownMenu = d3.select("#selDataset2");
  // Assign the value of the dropdown menu option to a variable
  var dataset = dropdownMenu.property("value");
  // console.log(dataset);
  updatePlot(dataset, 2);
}

// Function to build the plots
function buildPlot(country_id1, country_id2) {
  
  var year1 = ["1960", "1965", "1970", "1975", "1980", "1985", "1990", "1995", "2000", "2005", "2010", "2015"]; 
  var emissions1 = []; emissions2 = []; 
  var trace1 = [];
  var trace2 = [];

  var url =
  `http://localhost:5000/api/v1/resources/emissions/country?id=${country_id1}`;

  d3.json(url).then(function(data) {
    
    emissions1.push(data[0]["1960"]);
    emissions1.push(data[0]["1965"]);
    emissions1.push(data[0]["1970"]);
    emissions1.push(data[0]["1975"]);
    emissions1.push(data[0]["1980"]);
    emissions1.push(data[0]["1985"]);
    emissions1.push(data[0]["1990"]);
    emissions1.push(data[0]["1995"]);
    emissions1.push(data[0]["2000"]);
    emissions1.push(data[0]["2005"]);
    emissions1.push(data[0]["2010"]);
    emissions1.push(data[0]["2015"]);

    trace1 = {
      mode: "lines",
      name: data[0].country,
      x: year1,
      y: emissions1,
      line: {
        color: "#17BECF"
      }
    };
  });

  url = `http://localhost:5000/api/v1/resources/emissions/country?id=${country_id2}`;

  d3.json(url).then(function(data) {

    emissions2.push(data[0]["1960"]);
    emissions2.push(data[0]["1965"]);
    emissions2.push(data[0]["1970"]);
    emissions2.push(data[0]["1975"]);
    emissions2.push(data[0]["1980"]);
    emissions2.push(data[0]["1985"]);
    emissions2.push(data[0]["1990"]);
    emissions2.push(data[0]["1995"]);
    emissions2.push(data[0]["2000"]);
    emissions2.push(data[0]["2005"]);
    emissions2.push(data[0]["2010"]);
    emissions2.push(data[0]["2015"]);

    trace2 = {
      mode: "lines",
      name: data[0].country,
      x: year1,
      y: emissions2,
    };
  });

  var datatr = [trace1, trace2];
  console.log(trace1);
  var layout = {
    title: {
      text:`Emissions Comparison by Country`,
      font: {
        family: 'Courier New, monospace',
        size: 24,
        color: 'black',
        fontWeight: 'bold'
      }
    },
    xaxis: {
      title: {
        text: 'Year',
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: 'black',
          fontWeight: 'bold'
        }
      }
    },

    yaxis: {
      title: {
        text: 'CO2 emissions (kt)',
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: 'black',
          fontWeight: 'bold'
        }
      }
    },
    plot_bgcolor:"#fefcf7",
    paper_bgcolor:"#dce1e2"
  };
    
  Plotly.newPlot("plot", datatr, layout);
     
      // var trace1 = {
      //   x: year1,
      //   y: percentages1,
      // };

      // var trace2 = {
      //   x: year2,
      //   y: percentages2,
      // };

    

      // var data_update = [trace1, trace2, trace3, trace4, trace5];

      // var layout_update = {
      //   title: `${country} - Electricity Generation by Source (% of total)`, // updates the title
      // };

      // Plotly.relayout("plot", layout_update);
      // if (plotId == 1) {
      //   Plotly.update("plot", [year1], layout_update, 0)
      //   Plotly.restyle("plot", "x", [year1]);
      //   Plotly.restyle("plot", "y", [percentages1]);
      // }
      // else {
      //   Plotly.update("plot2", [year1], layout_update, 0)
      //   Plotly.restyle("plot2", "x", [year1]);
      //   Plotly.restyle("plot2", "y", [percentages1]);        
      // }

  
}

init();
