/* 
Based upon code of Martin Bostock, 2010
Web: https://github.com/mbostock/

Somewhat extended by Hernani Marques <h2m@access.uzh.ch>, 2013
to meet wh4t's needs
*/

var w = 700, // initially 800
    h = 700, // initially less
    fill = d3.scale.category10(); // initially 20

function redraw() {
  vis.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
  vis.attr("font-size", (nodeFontSize / d3.event.scale) + "px");
  vis.selectAll("line.link").style("stroke-width", getStrokeWidth); // Function so it runs for each element individually
}

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h)
  .append("svg:svg")
    .call(d3.behavior.zoom().on("zoom", redraw))
  .append("svg:svg");


d3.json("wh4t_graph.json", function(json) {

  var force = d3.layout.force()
      .charge(-14) // Regulates distance
      .linkDistance(100) // initially 50
      .nodes(json.nodes)
      .links(json.links)
      .size([w, h])
      .start();

  var link = vis.selectAll("line.link")
      .data(json.links)
    .enter().append("svg:line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return d.value * 2 ; })
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  var node = vis.selectAll("g.node")
      .data(json.nodes)
    .enter().append("svg:g")
      .attr("class", "node")

      node.append("svg:circle")
      .attr("r", function(d) { return ((Math.sqrt(d.rawlen) + Math.log(d.rawlen))/2)/6 ; })
      .style("fill", function(d) { return fill(d.group); })
      .call(force.drag);

 node.append("title")
	.text(function(d) { return d.name; });

node.on("mouseover", on_mouseover);
node.on("mouseout", on_mouseout);

var doc_id = d3.select("#doc_id")
var group_no = d3.select("#group_no")
var cluster_stems = d3.select("#cluster_stems")
var stems = d3.select("#stems")
var words = d3.select("#words")

function on_mouseover(d)
{
	doc_id.html("<h5>"+d.id+"</h5>");
	group_no.html("<h4>"+d.group+"</h4>");
	
	// Print stems in formatted way
	stems_formatted = "<h4>" + 
                          format_array_to_html_str(d.uniq_stems) + 
                          "</h4>";
	stems.html(stems_formatted);


	if(d.cluster_stems) {
		cluster_stems_formatted = "<h4>" + 
                          format_array_to_html_str(d.cluster_stems) + 
                          "</h4>";
		cluster_stems.html(cluster_stems_formatted);
	}

	// Print words in formatted way
	words_formatted = "<h4>" +
                          format_array_to_html_str(d.words) + 
			  "</h4>";
	words.html(words_formatted);
	
	doc_id.transition().duration(200).style("opacity","1")
	// group_no.transition().duration(200).style("opacity","1")
	cluster_stems.transition().duration(200).style("opacity","1")
	stems.transition().duration(200).style("opacity","1")
	words.transition().duration(200).style("opacity","1")

	Tip(d.rawcontent, SHADOW, true, TITLE, d.subj, LEFT, true,
            OPACITY, 90, BGCOLOR, "yellow", FIX, [0,0], 
            FADEIN, 0, FADEOUT, 100, STICKY, true, CLICKCLOSE, true);

}

function format_array_to_html_str(arr)
{
	var str = "";

	len = arr.length;
	if (len > 10)
		len = 10;
		
        for (i=0; i<len; i++)
        {
                str += arr[i]+" ";
                if ( (i+1) % 3 == 0)
                        str+="<br />";
        }

	return str;
}

function on_mouseout(d)
{
	doc_id.transition().duration(1000).style("opacity","0")
	// group_no.transition().duration(1000).style("opacity","0")
	cluster_stems.transition().duration(1000).style("opacity","0")
	stems.transition().duration(1000).style("opacity","0")
	words.transition().duration(1000).style("opacity","0")
	UnTip();
}

  vis.style("opacity", 1e-6)
    .transition()
      .duration(1000)
      .style("opacity", 1);

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    
    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  });
});
