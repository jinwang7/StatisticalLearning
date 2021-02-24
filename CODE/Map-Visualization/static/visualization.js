// enter code to define margin and dimensions for svg
var margin = { top: 0, right: 50, bottom: 50, left: 100 };
var width = window.innerWidth - margin.left - margin.right;
var height = window.innerHeight - margin.top - margin.bottom - 100;
// enter code to create svg
var svg = d3
  .select("#map")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
// create projection for map
var projection = d3
  .geoAlbersUsa()
  .translate([width / 2, height / 2])
  .scale(1300);
var path = d3.geoPath().projection(projection);
// create zoom scale
var zoom = d3.zoom().scaleExtent([1, 5]).on("zoom", zoomed);
// enter code to define tooltip
var tip = d3
  .tip()
  .attr("class", "d3-tip")
  .html(function (d) {
    return (
      "<span><b>County:</b> " +
      d["name"] +
      "</span><br>" +
      "<span><b>Total number of accidents:</b> " +
      d["accidentNum"] +
      "</span><br>" +
      "<span><b>County median car accidents handling time(minutes):</b> " +
      Math.round(d["countyMedianHT"]) +
      "</span><br>" +
      "<span><b>State:</b> " +
      d["state"] +
      "</span>"
    );
  });
// load data from backend
var mapPromise = d3.json("/getMapData");
var countyPromise = d3.json("/getCountyData");
var getHT = d3.json("/getHTData");

Promise.all([mapPromise, countyPromise, getHT])
  .then((data) => {
    var usa = data[0];
    var county = data[1];
    var data = data[2];
    ready(usa, county, data);
  })
  .catch((error) => {
    console.log(error.message);
  });
// Get max number of accidents
function ready(state, county, data) {
  var maxAccNum = d3.max(data, function (d) {
    return d["accidentNum"];
  });
  var radius = d3.scaleSqrt().domain([0, maxAccNum]).range([0, 25]);
  var dropDownJunction = d3.select("#junctionList");
  var junctionOptions = ["Yes", "No"];

  dropDownJunction
    .selectAll("option")
    .data(junctionOptions)
    .enter()
    .append("option")
    .text(function (d) {
      return d;
    })
    .attr("value", function (d) {
      return d;
    });
  var states = topojson.feature(state, state.objects.states).features;
  var counties = topojson.feature(state, state.objects.counties).features;

  // match coordinate to county names
  for (let i = 0; i < counties.length; i++) {
    let id = counties[i]["id"].toString();
    if (id.length != 5) {
      id = "0" + id;
    }
    for (let j = 0; j < county.length; j++) {
      if (counties[i]["id"] === county[j]["fips"]) {
        counties[i]["name"] = county[j]["name"];
        counties[i]["state"] = county[j]["state"];
      }
    }
  }
  for (let i = 0; i < data.length; i++) {
    for (let j = 0; j < counties.length; j++) {
      if (
        counties[j]["name"] &&
        data[i]["county"] === counties[j]["name"].toLowerCase() &&
        data[i]["state"] === counties[j]["state"]
      ) {
        counties[j]["accidentNum"] = data[i]["accidentNum"];
        counties[j]["countyMedianHT"] = data[i]["countyMedianHT"];
      }
    }
  }
  // svg draw states on map
  svg
    .selectAll(".state")
    .data(states)
    .enter()
    .append("path")
    .attr("class", "state")
    .attr("d", path);
  // svg draw counties on map
  svg
    .selectAll(".county")
    .data(counties)
    .enter()
    .append("path")
    .attr("class", "county")
    .attr("d", path);
  // draw bubble for each counties
  svg
    .append("g")
    .attr("class", "bubble")
    .selectAll("circle")
    .data(counties)
    .enter()
    .append("circle")
    .attr("transform", function (d) {
      return "translate(" + path.centroid(d) + ")";
    })
    .attr("r", function (d) {
      return radius(d["accidentNum"]);
    })
    .on("click", clicked)
    .on("mouseout", tip.hide);

  var legend = svg
    .append("g")
    .attr("class", "legend")
    .attr("transform", "translate(" + (width - 100) + "," + (height - 20) + ")")
    .selectAll("g")
    .data([100000, 200000, 300000])
    .enter();

  legend
    .append("circle")
    .attr("cy", function (d) {
      return -radius(d);
    })
    .attr("r", radius);

  legend
    .append("text")
    .attr("y", function (d) {
      return -2 * radius(d);
    })
    .attr("dy", "10px")
    .text(d3.format(".1s"));
}

// zoom in when double clicked
svg.call(zoom);
function zoomed() {
  svg.selectAll("path").attr("transform", d3.event.transform);
  svg.selectAll(".bubble").attr("transform", d3.event.transform);
}
// display detailed county accident information
svg.call(tip);
function clicked(d) {
  tip.show(d);
  var toolTip = d3.select(".d3-tip");
  toolTip.style("opacity", "0.8");
}
function handleSubmit() {
  var date = document.getElementById("date").value;
  var temperature = document.getElementById("temperature").value;
  var junction = document.getElementById("junctionList").value;
  var zipcode = document.getElementById("zipcode").value;
  if (junction === "Yes") {
    junction = 1;
  } else {
    junction = 0;
  }
  var queryHT = d3.json(
    `/getHTData?zip=${zipcode}&date=${date}&temperature=${temperature}&junction=${junction}`
  );
  Promise.all([queryHT])
    .then((queryData) => {
      showPrediction(queryData[0]);
    })
    .catch((error) => {
      alert("Incomplete or inaccurate inputs. Please check your input.");
      console.log(error.message);
    });
}

function showPrediction(result) {
  alert(
    "County: " +
      result.county.charAt(0).toUpperCase() +
      result.county.slice(1) +
      "\nState: " +
      result.state +
      "\nZip Code: " +
      result.zip +
      "\nPredicted Car Accident Handling Time: " +
      Math.round(result["HT"]) +
      " minutes"
  );
}
