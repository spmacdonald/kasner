var dim = 500,
    strokeWidth = "1.5px",
    initialPoint = [{x: mapTransform(0.963525), y: mapTransform(0.267617)}],
    triangle_lines = [{x1: 2, y1: 0, x2: -1, y2: 1.73205080},
                      {x1: 2, y1: 0, x2: -1, y2: -1.73205080},
                      {x1: -1, y1: -1.73205080, x2: -1, y2: 1.73205080}];


var svg = d3.select("#vis").append("svg:svg")
    .attr("width", dim)
    .attr("height", dim)
    .attr("viewBox", "0 0 500 500");


var line = svg.selectAll("line")
    .data(triangle_lines)
  .enter().append("svg:line")
    .attr("x1", function(d) { return mapTransform(d.x1); })
    .attr("x2", function(d) { return mapTransform(d.x2); })
    .attr("y1", function(d) { return mapTransform(d.y1); })
    .attr("y2", function(d) { return mapTransform(d.y2); })
    .attr("vector-effect", "non-scaling-stroke")
    .attr("stroke-width", strokeWidth)
    .attr("stroke", "black")
    .attr("stroke-linecap", "round")


var circle = svg.append("svg:circle")
    .attr("cx", mapTransform(0))
    .attr("cy", mapTransform(0))
    .attr("r", mapScale(1))
    .attr("fill", "none")
    .attr("stroke", "black")
    .attr("stroke-width", strokeWidth)


svg.selectAll("circle.control")
    .data(initialPoint)
  .enter().append("svg:circle")
    .attr("class", "control")
    .attr("r", 7)
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .call(d3.behavior.drag()
      .on("dragstart", function(d) {
        this.__origin__ = [d.x, d.y];
      })
      .on("drag", function(d) {
        r = mapScale(1);
        x = invMapTransform(Math.min(dim, Math.max(0, this.__origin__[0] += d3.event.dx)));
        y = invMapTransform(Math.min(dim, Math.max(0, this.__origin__[1] += d3.event.dy)));
        angle = Math.atan2(y, x);
        d.x = mapTransform(Math.cos(angle));
        d.y = mapTransform(Math.sin(angle));
        // update();
        svg.selectAll("circle.control")
          .attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });
      })
      .on("dragend", function() {
        delete this.__origin__;
      }));


// For debugging
var rect = svg.append("svg:rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", dim)
    .attr("height", dim)
    .attr("fill", "none")
    .attr("stroke", "black")


function mapScale(x) {
    return (dim / 4) * x;
}

function mapTransform(x) {
    return dim / 4 * (x + 2);
}

function invMapTransform(x) {
    return 4 * x / dim - 2;
}
