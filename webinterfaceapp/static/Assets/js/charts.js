function initializeBubbleChart() {
    var diameter = 400;
    var bubbleSvg = d3.select("#bubbleChart")
        .append("svg")
        .attr("width", diameter)
        .attr("height", diameter)
        .attr("class", "bubble");
    return bubbleSvg;
}


// function initializePieChart(){
//
//         var width = 500,
//       height = 500,
//       radius = Math.min(width, height) / 2;
//
//       var pieSvg = d3.select("#pieChart")
//       .append("svg")
//         .attr("width", width)
//         .attr("height", height)
//       .append("g")
//         .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
//
//       return pieSvg;
// }


function bubbleChart(dataset, svg) {
    svg.selectAll("*").remove();

    //console.log(dataset)

    var diameter = 400;
    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var bubble = d3.pack(dataset)
        .size([diameter, diameter])
        .padding(1.5);


    var nodes = d3.hierarchy(dataset)
        .sum(function (d) {
            return d.Count;
        });

    var node = svg.selectAll(".node")
        .data(bubble(nodes).descendants(), function (d) {
            return d.Name
        })


    var nodeEnter = node.enter()
        .filter(function (d) {
            return !d.children
        })
        .append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });


    nodeEnter.append("title")
        .text(function (d) {
            return d.Name + ": " + d.Count;
        });

    nodeEnter.append("circle")
        .attr("r", function (d) {
            return d.r;
        })
        .style("fill", function (d, i) {
            return color(i);
        });

    nodeEnter.append("text")
        .attr("dy", ".2em")
        .style("text-anchor", "middle")
        .text(function (d) {
            return d.data.Name.substring(0, d.r / 3);
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", function (d) {
            return d.r / 5;
        })
        .attr("fill", "white");

    nodeEnter.append("text")
        .attr("dy", "1.3em")
        .style("text-anchor", "middle")
        .text(function (d) {
            return d.data.Count;
        })
        .attr("font-family", "Gill Sans", "Gill Sans MT")
        .attr("font-size", function (d) {
            return d.r / 5;
        })
        .attr("fill", "white");

    nodeEnter.transition().attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

    node.exit().remove();

    d3.select(self.frameElement)
        .style("height", diameter + "px");

}

function doughnutChartCustom(word) {

    var label = [];
    var count = [];

    var i;

    for (i = 0; i < word.length; i++) {

        count.push(parseInt(word[i].Count));
        label.push(word[i].Name);

        console.log(label);
        console.log(count);
    }

    new Chart(document.getElementById("doughnutChart"), {
        type: 'doughnut',
        data: {
            labels: label,
            datasets: [
                {
                    label: "Twitter data",
                    backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850", "#00AE24", "#463239", "#ff7700", "#e1001e", "#007a6a"],
                    data: count
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Predicted world population (millions) in 2050'
            }
        }
    });
}


function doughnutChart(word) {

    var dataList = {};
    var i;

    for (i = 0; i < word.length; i++) {
        dataList['y'] = parseInt(word[i].Count);
        dataList['label'] = word[i].Name;

        console.log(dataList);
    }

    var chart = new CanvasJS.Chart("doughnutChart", {
        animationEnabled: true,
        title: {
            text: "",
            horizontalAlign: "left"
        },
        data: [{
            type: "doughnut",
            startAngle: 60,
            //innerRadius: 60,
            indexLabelFontSize: 17,
            indexLabel: "{label} - {y}",
            toolTipContent: "<b>{label}:</b> {y}",
            dataPoints: dataList
        }]
    });
    chart.render();

}


// function pieChart(data,svg){
//
//     var keys = [
//       "White"
//       , "Unknown"
//       , "Black or African American"
//       , "American Indian or Alaska Native"
//       , "Asian"
//       , "Native Hawaiian "
//       , "Other Pacific Islander"
//       , "Native Islander"
//       , "Native or Pacific Islander"
//       , "Native Hawaiian Pacific Islander"];
//
//     var width = 250,
//       height = 250,
//       radius = Math.min(width, height) / 2;
//
//
//     svg.append("g").attr("class", "slices");
//
//     var pie = d3.pie()
//       .sort(null)
//       .value(function(d) {
//         return d.value;
//       });
//
//     var arc = d3.arc()
//       .outerRadius(radius * 1.0)
//       .innerRadius(radius * 0.0);
//
//     var outerArc = d3.arc()
//       .innerRadius(radius * 2.0)
//       .outerRadius(radius * 2.0);
//
//     var key = function(d) { return d.data.label; };
//
//     var color = d3.scaleOrdinal(d3.schemePastel1)
//         .domain(keys);
//
//     update(makeData(data));
//
// //    var inter = setInterval(function() {
// //        update(makeData());
// //      }, 2000);
//
//     function mergeWithFirstEqualZero(first, second){
//
//       var secondSet = d3.set();
//
//       second.forEach(function(d) { secondSet.add(d.label); });
//
//       var onlyFirst = first
//         .filter(function(d){ return !secondSet.has(d.label) })
//         .map(function(d) { return {label: d.label, value: 0}; });
//
//       var sortedMerge = d3.merge([ second, onlyFirst ])
//         .sort(function(a, b) {
//             return d3.ascending(a.label, b.label);
//           });
//
//       return sortedMerge;
//     }
//
//     function makeData(data) {
//
//       var _data = Array();
//
//       for (i = 0; i < 10; i++) {
//
//           var ob = {};
//           ob["label"] = data[i]['Name'];
//           ob["value"] = data[i]['Count'];
//           _data.push(ob);
//
//       }
//
//       var sortedData = _data.sort(function(a, b) {
//           return d3.ascending(a.label, b.label);
//         });
//
//       return sortedData;
//     }
//
//     function randomCount(min, max) {
//
//       return Math.floor(Math.random() * (max - min + 1)) + min;
//     }
//
//     function update(data) {
//
//         var duration = 500;
//
//         var oldData = svg.select(".slices")
//           .selectAll("path")
//           .data().map(function(d) { return d.data });
//
//         if (oldData.length == 0) oldData = data;
//
//         var was = mergeWithFirstEqualZero(data, oldData);
//         var is = mergeWithFirstEqualZero(oldData, data);
//
//         var slice = svg.select(".slices")
//           .selectAll("path")
//           .data(pie(was), key);
//
//         slice.enter()
//           .insert("path")
//           .attr("class", "slice")
//           .style("fill", function(d) { return color(d.data.label); })
//           .each(function(d) {
//               this._current = d;
//             });
//
//         svg.selectAll("#pieChart")
//             .data(pie(is), key)
//             .enter().append("text")
//             .style("fill", "black")
//           .style("font-size", "13px")
//             .attr("y", function(d, i){ return -(i*20);}) //Move the text down
//           .attr("text-anchor", "middle")
// //            .text(function(d){return d.data.label;});
//
//
//         slice = svg.select(".slices")
//           .selectAll("path")
//           .text(function(d) { return d.data.label; })
//           .data(pie(is), key);
//
//
//
//
//
//         slice.transition()
//           .duration(duration)
//           .attrTween("d", function(d) {
//               var interpolate = d3.interpolate(this._current, d);
//               var _this = this;
//               return function(t) {
//                   _this._current = interpolate(t);
//                   return arc(_this._current);
//                 };
//             });
//
//
//         svg.select(".slices")
//           .selectAll("path")
//           .text(function(d) { return d.data.label; })
//           .data(pie(is), key);
//
//
//
//
//         slice.exit()
//           .transition()
//           .delay(duration)
//           .duration(0)
//           .remove();
//
//
//
//
//
//
//     };
// }






