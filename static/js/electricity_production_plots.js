
// Electricity Production Plots

/* global Plotly */
var source = ['Oil, gas and coal', 'Renewable sources, excluding hydroelectric', 'Nuclear', 'Natural Gas', 'Hydroelectric'];

// Display the default plot
function init() {
  
  addCountryDropDown ();
  // document.getElementById("selDataset2").style.display = "none";
  buildPlot("AU", true, 1);
  // document.getElementById("extraPlot").style.display = "none";
  buildPlot("NO", true, 2);

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
// Compare checkbox
d3.selectAll("#compareCountry").on("change", compareData);
// 2nd Country Dropdown
d3.selectAll("#selDataset2").on("change", getData2);

// Functions called by DOM changes
function getData() {
  var dropdownMenu = d3.select("#selDataset");
  // Assign the value of the dropdown menu option to a variable
  var dataset = dropdownMenu.property("value");
  // console.log(dataset);
  buildPlot(dataset, true, 1);
}

function compareData() {
  var countryCompare = document.getElementById("compareCountry").checked;
  // console.log(countryCompare);
  if (countryCompare) {
    document.getElementById("selDataset2").style.display = "block";
    document.getElementById("extraPlot").style.display = "block";
    buildPlot(dataset, true, 2);

  }
  else {
      document.getElementById("selDataset2").style.display = "none";
      document.getElementById("extraPlot").style.display = "none";
  }
}

function getData2() {
  var dropdownMenu = d3.select("#selDataset2");
  // Assign the value of the dropdown menu option to a variable
  var dataset = dropdownMenu.property("value");
  // console.log(dataset);
  buildPlot(dataset, true, 2);
}

// Function to build the plots
function buildPlot(country_id, isInit, plotId) {
  
  var year1 = []; var year2 = []; var year3 = []; var year4 = []; var year5 = [];
  var percentages1 = []; percentages2 = []; percentages3 = []; percentages4 = []; percentages5 = [];

  var url =
  `http://localhost:5000/api/v1/resources/electricity_production_values/country?id=${country_id}`;

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

    if (isInit) {

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
        title: {
          text:`${country} - Electricity Generation by Source (% of total)`,
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
            text: 'Percentage',
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
      if (plotId == 1) {Plotly.newPlot("plot", datatr, layout);}
      else {Plotly.newPlot("plot2", datatr, layout);}
      
    }
    
    else { 

      var trace1 = {
        x: year1,
        y: percentages1,
      };

      var trace2 = {
        x: year2,
        y: percentages2,
      };

      var trace3 = {
        x: year3,
        y: percentages3,
      };

      var trace4 = {
        x: year4,
        y: percentages4,
      };

      var trace5 = {
        x: year5,
        y: percentages5,
      };

      var data_update = [trace1, trace2, trace3, trace4, trace5];

      var layout_update = {
        title: `${country} - Electricity Generation by Source (% of total)`, // updates the title
      };

      // Plotly.relayout("plot", layout_update);
      if (plotId == 1) {
        Plotly.update("plot", [year1], layout_update, 0)
        Plotly.restyle("plot", "x", [year1]);
        Plotly.restyle("plot", "y", [percentages1]);
      }
      else {
        Plotly.update("plot2", [year1], layout_update, 0)
        Plotly.restyle("plot2", "x", [year1]);
        Plotly.restyle("plot2", "y", [percentages1]);        
      }
    }

  });
}

init();
