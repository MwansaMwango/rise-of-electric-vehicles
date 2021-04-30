// Declare variable to store market data
var marketShareData = [];
var datasetList = [];
var top5 = [];
var bottom5 = [];

// Get market share data slice relevant data
function init() {
  var url = "api/v1/resources/market-share";
  d3.json(url).then((data) => {
    marketShareData = data;
    console.log("marketShareData", marketShareData);
    //Get top 10 countries
    top10Countries = marketShareData.slice(0, 10).map((data) => data.Country);
    console.log("top10Countries", top10Countries);
    // Add countries to DOM dropdown menu
    top10Countries.forEach((country) => {
      d3.select("#selCountry-marketShare").append("option").text(country);
    });
    // Top 5
    top5 = marketShareData.slice(0, 5);
    console.log("top5", top5);
    // Bottom 5
    bottom5 = marketShareData.slice(0, 21).slice(-5);
    console.log("bottom5", bottom5);
    // Global Average
    globalAvg = marketShareData.slice(-1)[0];
    console.log("globalAvg", globalAvg);

    // Build plot
    buildPlot(marketShareData);
  });
}

// Function called by DOM changes
function handleChange(event) {
  d3.event.preventDefault();

  var newDatasetList = [];

  var eventTarget = d3.event.target;
  var eventTargetVal = eventTarget.value;

  // Check inputs
  console.log("eventTarget", eventTarget);
  console.log("eventTargetVal", eventTargetVal);

  // Apply filters to datasets according to selected filters

  if (eventTargetVal === "top5") {
    console.log("top5 selected");
    newDatasetList = top5;
  } else if (eventTargetVal === "bottom5") {
    console.log("bottom5 selected");
    newDatasetList = bottom5;
  } else if (eventTargetVal === "Select Country(All)") {
    newDatasetList.push(marketShareData.slice(0, 21));
    console.log("All selected");
  } else {
    marketShareData.forEach((dataset) => {
      if (dataset.Country === eventTargetVal) {
        newDatasetList.push(dataset);
        console.log("Country selected");
        // Clear radio button
        eventTargetVal = "";
      }
    });
  }

  console.log("newDatasetList", newDatasetList);
  // Call function to update the chart
  buildPlot(newDatasetList);
}

function buildPlot(datasetList) {
  var datatr = [];
  for (i = 0; i < datasetList.length; i++) {
    datatr.push({
      type: "scatter",
      mode: "lines",
      name: datasetList[i].Country,
      x: Object.keys(datasetList[i]).slice(0, 8), //years
      y: Object.values(datasetList[i]).slice(0, 8), //percentages
    });
  }

  // var layout = {
  //   title: `EV Market Share of All New Car Sales`,
  //   xaxis: {
  //     title: "Year",
  //   },
  //   yaxis: {
  //     autorange: true,
  //     type: "linear",
  //     title: "Percentage %",
  //   },
  //   width: "70vw",
  //   height: "60vh",
  //   paper_bgcolor: "smoker",
  //   font: { color: "blue", family: "Arial" },
  // };

  var layout = {
    title: {
      text: `EV Market Share of All New Car Sales`,
      font: {
        family: "Courier New, monospace",
        size: 24,
        color: "black",
        fontWeight: "bold",
      },
    },
    xaxis: {
      title: {
        text: "Year",
        font: {
          family: "Courier New, monospace",
          size: 18,
          color: "black",
          fontWeight: "bold",
        },
      },
    },

    yaxis: {
      title: {
        text: "Percentage %",
        font: {
          family: "Courier New, monospace",
          size: 18,
          color: "black",
          fontWeight: "bold",
        },
      },
    },
    width: "70vw",
    height: "60vh",
    plot_bgcolor: "#fefcf7",
    paper_bgcolor: "#dce1e2",
  };
  Plotly.newPlot("market-share-plot", datatr, layout);
}
// On dropdown change to the DOM, call handleChange
d3.selectAll("#selCountry-marketShare").on("change", handleChange);
// On check input change to the DOM, call handleChange
d3.selectAll(".form-check-input").on("change", handleChange);

init();
