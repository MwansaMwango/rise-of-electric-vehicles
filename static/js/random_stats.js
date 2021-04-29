    // Variables to hold data from random stat generator api
    var url = "api/v1/resources/get-random-stat";
    var randomStatBtn = d3.select("#statBtn");
    // Function to handle get random stat button
    function handleClick(event) {
      d3.event.preventDefault();
      console.log("clicked NEW");
      d3.json(url).then(data => {
          // Update Statistic text
          d3.select("#statText").text(data);
          // Update Button Text
          d3.select("#statBtn").text("Need More Facts?");   
      })
    }
    // Listen for random stat button click event
    randomStatBtn.on("click", handleClick);