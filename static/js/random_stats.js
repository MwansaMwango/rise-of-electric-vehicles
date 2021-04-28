    // Variables to hold data from random stat generator api
    var randomStat;
    var url = "http://localhost:5000/api/v1/resources/get-random-stat";
    var randomStatBtn = d3.select("#statBtn")
    // Function to handle get random stat button
    function handleClick(event) {
      d3.event.preventDefault();

      d3.json(url).then(data => {
          randomStat = data
          // Statistic text
          d3.select("#statText").text(randomStat);
          // Button Text
          d3.select("#statBtn").text("Need More?");
          console.log("Clicked");
      })

    }

    // Listen for random stat button click event
    randomStatBtn.on("click", handleClick);