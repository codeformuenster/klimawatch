function clamp(a, b, c){ return Math.max(a, Math.min(b, c)) }

var data = {{ jsonify .values }};

function initYouDrawIt() {
  var ƒ = d3.f;

  var sel = d3.select('#{{ .chart_id }}').html('')
  var c = d3.conventions({
    parentSel: sel,
    totalWidth: sel.node().offsetWidth,
    height: 400,
    margin: {left: 100, right: 50, top: 30, bottom: 30}
  })

  c.svg.append('rect').at({width: c.width, height: c.height, opacity: 0})

  c.x.domain([{{ .start_year_chart }}, {{ .end_year_chart }}])
  c.y.domain([{{ .min_value }}, {{ .max_value }}])

  c.xAxis.ticks({{ .year_label_ticks }}).tickFormat(ƒ())
  c.yAxis.ticks({{ .value_label_ticks }}).tickFormat(d => d + " {{ .unit }}")

  var area = d3.area().x(ƒ('year', c.x)).y0(ƒ('value', c.y)).y1(c.height)
  var line = d3.area().x(ƒ('year', c.x)).y(ƒ('value', c.y))

  var clipRect = c.svg
    .append('clipPath#clip')
    .append('rect')
    .at({width: c.x({{ .start_year_draw }}) - 2, height: c.height})

  var correctSel = c.svg.append('g').attr('clip-path', 'url(#clip)')

  correctSel.append('path.area').at({d: area(data)})
  correctSel.append('path.line').at({d: line(data)})
  yourDataSel = c.svg.append('path.your-line')

  c.drawAxis()

  yourData = data
    .map(function(d){ return {year: d.year, value: d.value, defined: 0} })
    .filter(function(d){
      if (d.year == {{ .start_year_draw }}) d.defined = true
      return d.year >= {{ .start_year_draw }}
    })

  var completed = false

  var drag = d3.drag()
    .on('drag', function(){
      var pos = d3.mouse(this)
      var year = clamp({{ .start_year_draw  }}+1, {{ .end_year_chart }}, c.x.invert(pos[0]))
      var value = clamp(0, c.y.domain()[1], c.y.invert(pos[1]))

      yourData.forEach(function(d){
        if (Math.abs(d.year - year) < .5){
          d.value = value
          d.defined = true
        }
      })

      yourDataSel.at({d: line.defined(ƒ('defined'))(yourData)})

      if (!completed && d3.mean(yourData, ƒ('defined')) == 1){
        completed = true
        clipRect.transition().duration(1000).attr('width', c.x({{ .end_year_chart }}))
      }
    })

  c.svg.call(drag)
};

window.addEventListener("load", function () {
  initYouDrawIt();
});
