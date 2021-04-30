/* Global Plotly */
var url = `api/v1/resources/tesla-sales`;

function buildPlot() {
  d3.json(url).then(function (data) {
    console.log("Data", data);
    tesla_sales_data = data;
    // Create your Bar plot trace.
    var trace1 = {
      x: tesla_sales_data.map((doc) => doc.Quarter),
      y: tesla_sales_data.map((doc) => doc.Total_Sales),
      type: "bar",
      //   orientation: "h",
      marker: {
        color: "rgba(25, 184, 22,0.6)",
        line: { width: 2 },
      },
    };
    //Create the data array for our plot
    var data = [trace1];
    //Define our plot layout
    // var layout = {

    // width: 1200,
    // height: 800,
    // plot_bgcolor:"#fefcf7",
    // paper_bgcolor:"#dce1e2"
    // };

    var layout = {
      title: {
        text: "Tesla Quarterly Sales & Production",
        font: {
          family: "Courier New, monospace",
          size: 24,
          color: "black",
          fontWeight: "bold",
        },
      },
      xaxis: {
        title: {
          text: "Quarter / Year",
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
          text: "Electric Vehicles Sold",
          font: {
            family: "Courier New, monospace",
            size: 18,
            color: "black",
            fontWeight: "bold",
          },
        },
      },
    //   width: 1200,
      height: 800,
      plot_bgcolor: "#fefcf7",
      paper_bgcolor: "#dce1e2",
    };
    //Plot the chart to a div tag with id "bar"
    Plotly.newPlot("bar", data, layout);
  });
}

buildPlot();
