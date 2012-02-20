// XXX: Test when rotate on iPhone!

var dim = 500,
    strokeWidth = "1.5px",
    numPoints = 3,
    initialPoint = [{x: mapTransform(0.963525), y: mapTransform(0.267617)}],
    triangleVerticies = [{x: mapTransform(2), y: mapTransform(0)},
                       {x: mapTransform(-1), y: mapTransform(1.73205080)},
                       {x: mapTransform(-1), y: mapTransform(-1.73205080)}],
    triangleLines = [{x1: 2, y1: 0, x2: -1, y2: 1.73205080},
                      {x1: 2, y1: 0, x2: -1, y2: -1.73205080},
                      {x1: -1, y1: -1.73205080, x2: -1, y2: 1.73205080}];


var svg = d3.select("#vis").append("svg:svg")
    .attr("width", dim)
    .attr("height", dim)
    .attr("viewBox", "0 0 500 500");


var line = svg.selectAll("line")
    .data(triangleLines)
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
        update(d.x, d.y);
        svg.selectAll("circle.control")
          .attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });
      })
      .on("dragend", function() {
        delete this.__origin__;
      }));


function update(x, y) {
    var p = circle_line_intersection({x:x, y:y}, triangleVerticies[0]);
    console.log(p);
    var line = svg.append("svg:line")
        .attr("x1", x)
        .attr("x2", mapTransform(p.x))
        .attr("y1", y)
        .attr("y2", mapTransform(p.y))
        .attr("vector-effect", "non-scaling-stroke")
        .attr("stroke-width", strokeWidth)
        .attr("stroke", "black")
        .attr("stroke-linecap", "round")
}


function circle_line_intersection(p, v) {
    // console.log(p.x + " " + v.x + " " + p.y + " " + v.y);
    // Map to local user coords (circle centered at 0,0).
    px = invMapTransform(p.x);
    py = invMapTransform(p.y);
    vx = invMapTransform(v.x);
    vy = invMapTransform(v.y);

    dx = vx - px;
    dy = vy - p.y;
    dr = dx * dx + dy * dy;
    d = px * vy - vx * py;
    disc = dr - d * d;

    // XXX: Test for tangent (disc == 0)
    if (disc > 0) {
        disc = Math.sqrt(disc);

        x0 = (d * dy + sgn(dy) * dx * disc) / dr;
        y0 = (-d * dx + Math.abs(dy) * disc) / dr;
        if ( !almost_equal(x0, px) || !almost_equal(y0, py) ) {
            return {x: x0, y: y0};
        }

        x0 = (d * dy - sgn(dy) * dx * disc) / dr;
        y0 = (-d * dx - Math.abs(dy) * disc) / dr;
        if ( !almost_equal(x0, px) || !almost_equal(y0, py) ) {
            return {x: x0, y: y0};
        }

        return false;
    }
}

function sgn(x) {
    if (x < 0) {
        return -1;
    }
    return 1;
}

function almost_equal(x, y) {
    if (Math.abs(x - y) < 0.0000001) {
        return true;
    }
    return false;
}

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
