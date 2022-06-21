// Start of document ready function
$(document).ready(function(){
    var _data;
    var _labels;

  // getyearsdropdown
  $.ajax({
    url: "/getyearsrange",
    type: "get",
    data: {vals: ''},
    success: function(response) {
      full_data = JSON.parse(response.yearsrange);
      for(const year of full_data) {
        var year2 = year;
        $("#years").append("<option value='"+year2+"'>"+year2+"</option>");

      }
     
    },
    async:false
  });
  
  // Sort By year when page load
  $.ajax({
    url: "/data",
    type: "get",
    data: {vals: ''},
    success: function(response) {
      full_data = JSON.parse(response.tweets);
      
      _data = full_data['data'];
      _labels = full_data['labels'];
    },
    async:false
  });
  var config = {
    type: 'bar',
    data: {
        labels:_labels,
        datasets: [{
            label: "# of Twitter Messages Per Year",
            data: _data,
            backgroundColor:["#d3c368"]
        }]
    }




  };

  // Declare new Chart
  var ctx = document.getElementById("barChart");
  var charts = new Chart(ctx,config);

  // Pass chart to chartbymonth function
  chartbymonth(charts);
 

 });
 // End of document ready function


// Chartbymonth function start

function chartbymonth(charts){

// Get selected value
var selectedyear = document.getElementById("years").value;

// Re-declare var
var _data;
var _labels;

// Condition if the selected value is not = to "all"
 if (selectedyear != "all") {
   // Post the selected value to server (app.py) to run "query" with ajax
  $.ajax({
    url: "/getdashboardpermonth",
    type: "POST",
    data: JSON.stringify({"year": selectedyear}),
    success: function(response) {
      // Post sucessful then use ajax again to get return data from server (app.py)
      $.ajax({
        url: "/getdashboardpermonth",
        type: "get",
        data: {vals: ''},
        success: function(response) {
          full_data = JSON.parse(response.tweets);
          
        
        },
        async:false
      });
      // if sucessful pass in to chartbymonth2
      full_data2 = JSON.parse(response.tweets);
      chartbymonth2(full_data2,charts);
    },
    async:false
  });
}
else {
  // if selected year is = to "all" get from "/data" then pass to chartbyyear2
  $.ajax({
    url: "/data",
    type: "get",
    data: {vals: ''},
    success: function(response) {
      full_data3 = JSON.parse(response.tweets);
      chartbyyear2(full_data3,charts);

    },
    async:false
  });


}
}
// Chartbyyear2 - gets data from chartbymonth if selected year = to "all"
function chartbyyear2(full_data,charts) {
  var _data = full_data["data"];
  var _labels = full_data["labels"];

  // remove chart and create again start
  $('#barChart').remove();
  $('#dashboardcontainer').append('<canvas id="barChart" width="400" height="400"></canvas>')
   
  var config2 = {
    type: 'bar',
    data: {
        labels:_labels,
        datasets: [{
            label: "# of Twitter Messages Per Year",
            data: _data,
            backgroundColor:["#d3c368"]
        }]
    }
};
  var ctx = document.getElementById("barChart");
  var charts = new Chart(ctx, config2);

  // remove chart and create again end

}

// Chartbymonth2 - gets data from chartbymonth if selected year != to "all"

function chartbymonth2(full_data,charts) {

  var _data = full_data["data"];
  var _labels = full_data["labels"];
  // remove chart and create again start
  $('#barChart').remove();
  $('#dashboardcontainer').append('<canvas id="barChart" width="400" height="400"></canvas>')
   
  var config2 = {
    type: 'bar',
    data: {
        labels:_labels,
        datasets: [{
            label: "# of Twitter Messages Per Month",
            data: _data,
            backgroundColor:["#d3c368"]
        }]
    }
};
  var ctx = document.getElementById("barChart");
  var charts = new Chart(ctx, config2);
  
  // remove chart and create again end


}



