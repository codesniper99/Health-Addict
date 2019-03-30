var _docHeight = (document.height !== undefined) ? document.height : document.body.offsetHeight;
        $(document).ready(function(){
            $('.toc-wrapper').pushpin({
                top: 290,
                offset: 100,
                bottom: _docHeight-600
            });
            $('.scrollspy').scrollSpy();
            $('.collapsible').collapsible({
                accordion:false,
            });
        });
        var size = 70,
        thickness = 30;
        var color = d3.scale.linear()
            .domain([0, 50, 100])
            .range(['#21ba45', '#fbbd08', '#db2828']);
        var arc = d3.svg.arc()
            .innerRadius(size - thickness)
            .outerRadius(size)
            .startAngle(-Math.PI / 2);
        var svg = d3.select('#chart').append('svg')
            .attr('width', size * 2)
            .attr('height', size + 20)
            .attr('class', 'gauge');
        var chart = svg.append('g')
            .attr('transform', 'translate(' + size + ',' + size + ')')
        var background = chart.append('path')
            .datum({
                endAngle: Math.PI / 2
            })
            .attr('class', 'background')
            .attr('d', arc);
        var foreground = chart.append('path')
            .datum({
                endAngle: -Math.PI / 2
            })
            .style('fill', '#db2828')
            .attr('d', arc);
        var scale = svg.append('g')
            .attr('transform', 'translate(' + size + ',' + (size + 15) + ')')
            .attr('class', 'scale');
        function update(v) {
            v = d3.format('.1f')(v);
            foreground.transition()
                .duration(750)
                .style('fill', function() {
                    return color(v);
                })
                .call(arcTween, v);

        }
        function arcTween(transition, v) {
            var newAngle = v / 100 * Math.PI - Math.PI / 2;
            transition.attrTween('d', function(d) {
                var interpolate = d3.interpolate(d.endAngle, newAngle);
                return function(t) {
                    d.endAngle = interpolate(t);
                    return arc(d);
                };
            });
        }
        function textTween(transition, v) {
            transition.tween('text', function() {
                var interpolate = d3.interpolate(this.innerHTML, v),
                    split = (v + '').split('.'),
                    round = (split.length > 1) ? Math.pow(10, split[1].length) : 1;
                return function(t) {
                    this.innerHTML = d3.format('.1f')(Math.round(interpolate(t) * round) / round) + '<tspan>%</tspan>';
                };
            });
        }

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight){
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}