$(document).ready(function(){


    var margin = {top: 0, right: 0, bottom: 0, left: 0},
        width = 960 - margin.left - margin.right,
        height = 800 - margin.top - margin.bottom,
        padding = 3;

    var projection = d3.geo.albers()
        .center([-1.165, 54.84])
        .rotate([4.4, 0])
        .parallels([50, 60])
        .scale(4000)
        .translate([width / 2, height / 2]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force().size([width, height]);

    d3.json("data/uk-constituency-centroids.json", function(error, constituencies) {

        var nodes = constituencies.features
            .filter(function(d) { return d.geometry.coordinates !== null })
            .map(function(d) {
                var point = projection(d.geometry.coordinates)
                return {
                  x: point[0], y: point[1],
                  x0: point[0], y0: point[1],
                  r: 4
                };
            });

        var links = [];

        var node = svg.selectAll("rect")
            .data(nodes)
            .enter().append("rect")
            .attr("width", function(d) { return d.r * 2; })
            .attr("height", function(d) { return d.r * 2; })
            .attr("x", function(d) { return d.x - d.r; })
            .attr("y", function(d) { return d.y - d.r; });

    });

});
