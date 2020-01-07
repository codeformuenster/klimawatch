(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('d3')) :
    typeof define === 'function' && define.amd ? define(['exports', 'd3'], factory) :
    (factory((global.youdrawit = {}),global.d3));
  }(this, (function (exports,d3) { 'use strict';
  
    var debounce = function debounce(func, wait, immediate) {
      var timeout = void 0;
      return function () {
        var context = this,
            args = arguments;
        var later = function later() {
          timeout = null;
          if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
      };
    };
  
    var ƒ = function ƒ() {
      var functions = arguments;
  
      //convert all string arguments into field accessors
      for (var i = 0; i < functions.length; i++) {
        if (typeof functions[i] === "string" || typeof functions[i] === "number") {
          functions[i] = function (str) {
            return function (d) {
              return d[str];
            };
          }(functions[i]);
        }
      }
  
      //return composition of functions
      return function (d) {
        var i = 0,
            l = functions.length;
        while (i++ < l) {
          d = functions[i - 1].call(this, d);
        }return d;
      };
    };
  
    var formatValue = function formatValue(val, unit, precision, defaultPrecision) {
      var data = precision ? Number(val).toFixed(precision) : defaultPrecision !== 0 ? Number(val).toFixed(defaultPrecision) : defaultPrecision === 0 ? Number(val).toFixed() : val;
      // revert decimal and thousands separator based on country
      var dataDelimited = numberWithCommas(data);
      if (getLanguage() === "de") {
        var temp1 = dataDelimited.replace(/\./g, "whatever");
        var temp2 = temp1.replace(/,/g, ".");
        dataDelimited = temp2.replace(/whatever/g, ",");
      } else if (getLanguage() === "fr") {
        var _temp = dataDelimited.replace(/\./g, "whatever");
        var _temp2 = _temp.replace(/,/g, " ");
        dataDelimited = _temp2.replace(/whatever/g, ",");
      }
      return dataDelimited + (unit ? " " + unit : "");
    };
  
    var numberWithCommas = function numberWithCommas(x) {
      var parts = x.toString().split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      return parts.join(".");
    };
  
    var clamp = function clamp(a, b, c) {
      return Math.max(a, Math.min(b, c));
    };
  
    function getRandom(min, max) {
      return Math.random() * (max - min) + min;
    }
  
    var yourData = "yourData";
    var resultShown = "resultShown";
    var completed = "completed";
    var score = "score";
    var predictionDiff = "predictionDiff";
    var prediction = "prediction";
    var truth = "truth";
  
    function compareGuess(truth$$1, guess, graphMaxY, graphMinY) {
      var maxDiff = 0;
      var predDiff = 0;
      truth$$1.forEach(function (ele, i) {
        maxDiff += Math.max(graphMaxY - ele.value, ele.value - graphMinY);
        predDiff += Math.abs(ele.value - guess[i].value);
      });
      return { maxDiff: maxDiff, predDiff: predDiff };
    }
  
    function getScore(key, truth$$1, state, graphMaxY, graphMinY, resultSection, scoreTitle, scoreButtonText, scoreButtonTooltip, scoreHtml) {
      var myScore = 0;
      var guess = state.getResult(key, yourData);
      var r = compareGuess(truth$$1, guess, graphMaxY, graphMinY);
      var maxDiff = r.maxDiff;
      var predDiff = r.predDiff;
      var scoreFunction = d3.scaleLinear().domain([0, maxDiff]).range([100, 0]);
  
      myScore = scoreFunction(predDiff).toFixed(1);
      state.set(key, predictionDiff, predDiff);
      state.set(key, score, +myScore);
  
      getFinalScore(key, state, resultSection, scoreTitle, scoreButtonText, scoreButtonTooltip, scoreHtml);
  
      console.log(state.get(key, yourData));
      console.log("The pred is: " + predDiff);
      console.log("The maxDiff is: " + maxDiff);
      console.log("The score is: " + myScore);
      console.log(state.getState());
    }
  
    function getFinalScore(key, state, resultSection, scoreTitle, scoreButtonText, scoreButtonTooltip, scoreHtml) {
      var completed$$1 = true;
      state.getAllQuestions().forEach(function (ele) {
        completed$$1 = completed$$1 && typeof state.get(ele, score) !== "undefined";
      });
      if (completed$$1) {
        var scores = 0;
        state.getAllQuestions().forEach(function (ele) {
          scores = scores + state.get(ele, score);
        });
        var finalScoreFunction = d3.scaleLinear().domain([0, 100 * state.getAllQuestions().length]).range([0, 100]);
        var finalScore = finalScoreFunction(scores).toFixed();
        console.log("The final score is: " + finalScore);
  
        drawScore(+finalScore, resultSection, key, scoreTitle, scoreButtonText, scoreButtonTooltip, scoreHtml);
      }
    }
  
    function drawScore(finalScore, resultSection, key, scoreTitle, scoreButtonText, scoreButtonTooltip, scoreHtml) {
      // add final result button
      var ac = resultSection.append("div").attr("class", "actionContainer finalScore");
      var button = ac.append("button").attr("class", "showAction");
      button.append("div").attr("class", "globals-scoreButtonText update-font").text(scoreButtonText);
  
      var tt = ac.append("div").attr("class", "tooltipcontainer").append("span").attr("class", "tooltiptext globals-scoreButtonTooltip update-font")
      //.attr("class", "tooltiptext")
      .text(scoreButtonTooltip);
  
      // add final result graph
      var fs = {};
      fs.div = resultSection.select("div.text").append("div").attr("class", "finalScore text").style("visibility", "hidden");
  
      fs.div.append("div")
      //.attr("class", "before-finalScore globals-scoreTitle update-font")
      .attr("class", "before-finalScore").append("strong").append("div").attr("class", "globals-scoreTitle update-font").text(scoreTitle);
  
      var svgWidth = window.innerWidth > 500 ? 500 : window.innerWidth - 10;
      fs.svg = fs.div.append("svg").attr("width", svgWidth).attr("height", 75);
  
      var ch = resultSection.select("div.text").append("div").attr("class", "customHtml").style("visibility", "hidden").style("text-align", "center");
  
      if (typeof scoreHtml !== "undefined") {
        var sHtml = scoreHtml.filter(function (d) {
          return d.lower <= finalScore && d.upper > finalScore;
        });
        ch.selectAll("p").data(sHtml).enter().append("p").append("div").attr("class", "globals-scoreHtml update-font").html(function (d) {
          return d.html;
        });
      }
  
      // adding some space at the bottom to reserved the final display space and 
      // to have space below the botton (for the tooltip) 
      // (30 = margin-top from fs.div) , 70 = margin-bottom from div.result.finished.shown)
      var h = fs.div.node().offsetHeight + ch.node().offsetHeight + 30 + 70 - ac.node().clientHeight;
      fs.div.style("display", "none").style("visibility", "visible"); // reset to avoid taking up space 
      ch.style("display", "none").style("visibility", "visible");
  
      var dummy = resultSection.append("div").attr("class", "dummy").style("height", h + "px");
  
      button.on("click", function () {
        d3.select("div.actionContainer.finalScore").style("display", "none");
        //d3.select(this).style("display", "none");
        tt.style("display", "none");
        dummy.remove();
        showFinalScore(finalScore, resultSection, key, svgWidth);
      });
    }
  
    function showFinalScore(finalScore, resultSection, key, svgWidth) {
  
      function showText() {
        d3.select(".result." + key).select("text.scoreText").style("opacity", 1);
        resultSection.select("div.customHtml").style("visibility", "visible");
      }
  
      resultSection.select("div.finalScore.text").style("display", "block");
      resultSection.select("div.customHtml").style("display", "block").style("visibility", "hidden");
  
      var fs = {};
  
      fs.g = resultSection.select(".finalScore.text > svg").append("g").attr("transform", "translate(5, 10)");
  
      // const xScale = d3.scaleLinear().domain([0, 100]).range([0, 400]);
      var xScale = d3.scaleLinear().domain([0, 100]).range([0, svgWidth - 80]);
      var xAxis = d3.axisBottom(xScale).ticks(4);
      fs.g.append("g").attr("transform", "translate(0, 45)").attr("class", "x axis").call(xAxis);
  
      fs.rect = fs.g.append("rect").attr("class", "final-score-result").attr("x", 0).attr("y", 0).attr("height", 40).attr("width", 0);
  
      fs.txt = fs.g.append("text").attr("class", "scoreText globals-scoreText update-font").attr("x", xScale(finalScore) + 5).attr("dy", 27).text("(" + finalScore + "/100)");
  
      fs.rect.transition().duration(3000).attr("width", xScale(finalScore)).on("end", showText);
    }
  
    /* 
     * params:
     * sel: DOM selection for the text label of the reference value. A <span> is added with the text
     * svg: SVG for the lines connecting the graph with the label
     * referenceValues: question.referenceValues
     * c: object constant with graphical DOM selections as properties
     */
    function addReferenceLines(sel, svg, referenceValues, c) {
      var gRef = void 0;
      var data = void 0;
      var referenceLine = d3.line().x(ƒ("year", c.x)).y(ƒ("value", c.y)).curve(d3.curveMonotoneX);
  
      referenceValues.forEach(function (ref, i) {
        data = ref.value.map(function (ele, index) {
          return {
            year: index,
            value: ele[Object.keys(ele)[0]]
          };
        });
        data.text = ref.text;
        data.anchor = parsePosition(ref.textPosition);
        data.offset = getOffset(data.anchor);
  
        gRef = svg.append("g").attr("class", "reference question-referenceValues referenceLine controls line-" + data.text.trim());
  
        gRef.append("path").attr("d", referenceLine(data)).attr("class", "line referencePath").attr("id", "curvedPath-" + i);
  
        gRef.append("text").attr("class", "question-referenceText update-font").attr("dy", "-5").append("textPath").attr("class", "referenceTextPath").attr("text-anchor", data.anchor).attr("startOffset", data.offset).attr("xlink:href", "#curvedPath-" + i).text(data.text);
      });
    }
  
    function parsePosition(pos) {
      if (pos !== "start" && pos !== "end") {
        pos = "middle";
      }
      return pos;
    }
  
    function getOffset(pos) {
      var offset = void 0;
      if (pos === "start") {
        offset = "2%";
      } else if (pos === "end") {
        offset = "98%";
      } else {
        offset = "50%";
      }
      return offset;
    }
  
    function addReferenceValuesDefault(sel, svg, referenceValues, c) {
      var gRef = void 0;
      var len = void 0;
  
      len = svg.select("g.grid").node().getBBox().width / 2;
  
      referenceValues.forEach(function (ref) {
        gRef = svg.append("g").attr("class", "reference question-referenceValues referenceLine controls");
  
        gRef.append("line").attr("x1", 0).attr("y1", c.y(ref.value)).attr("x2", len).attr("y2", c.y(ref.value)).attr("class", "line referencePath");
  
        sel.append("span").style("left", "10px").style("right", len - 10 + "px").style("top", c.y(ref.value) - 18 + "px").append("div").attr("class", "question-referenceValues update-font").style("text-align", "center").text(ref.text);
      });
    }
  
    /*
     * params:
     * sel: DOM selection for the text label of the reference value. A <span> is added with the text
     * svg: SVG for the lines connecting the graph with the label
     * referenceValues: question.referenceValues
     * c: object constant with graphical DOM selections as properties
     * line: true or false (= ticks)
     */
    function addReferenceValues(sel, svg, referenceValues, c, line) {
  
      if (line) {
        return addReferenceValuesDefault(sel, svg, referenceValues, c);
      }
      var len = 10;
      var shiftSpan = 8;
      var rectHeight = 30;
      var data = referenceValues.map(function (d) {
        return c.y(d.value) - shiftSpan;
      });
      var positions = getPositions(data, rectHeight, c.height);
      var gRef = void 0;
  
      referenceValues.forEach(function (ref, i) {
        gRef = svg.append("g").attr("class", "reference question-referenceValues controls");
  
        gRef.append("line").attr("x1", 0).attr("y1", c.y(ref.value)).attr("x2", len / 2).attr("y2", c.y(ref.value));
  
        gRef.append("line").attr("x1", len / 2).attr("y1", c.y(ref.value)).attr("x2", len).attr("y2", positions[i] + shiftSpan);
  
        sel.append("span").style("left", len + 3 + "px").style("top", positions[i] + "px").append("div").attr("class", "question-referenceValues update-font").text(ref.text);
      });
    }
  
    function getPositions(data, rectHeight) {
      var newPositions = void 0;
      var dataObject = createObject(data, rectHeight);
      dataObject = adjustBottoms(dataObject);
      newPositions = trimObject(dataObject);
      // drawRectangles(g, data2, "after");
  
      if (newPositions[newPositions.length - 1] < 0) {
        dataObject = adjustTops(dataObject);
        newPositions = trimObject(dataObject);
        // drawRectangles(g, data3, "final");
      }
      return newPositions;
    }
  
    function createObject(data, rectHeight, height) {
      // setup data structure with rectangles from bottom to the top
      var dataObject = [];
      var obj = { top: height, bottom: height + rectHeight }; // add dummy rect for lower bound
  
      dataObject.push(obj);
      data.forEach(function (d) {
        obj = { top: d, bottom: d + rectHeight };
        dataObject.push(obj);
      });
      obj = { top: 0 - rectHeight, bottom: 0 }; // add dummy rect for upper bound
      dataObject.push(obj);
  
      return dataObject;
    }
  
    function trimObject(dataObject) {
      // convert back to original array of values, also remove dummies
      var data3 = [];
      dataObject.forEach(function (d, i) {
        if (!(i === 0 || i === dataObject.length - 1)) {
          data3.push(d.top);
        }
      });
      return data3;
    }
  
    function adjustBottoms(dataObject) {
      dataObject.forEach(function (d, i) {
        if (!(i === 0 || i === dataObject.length - 1)) {
          var diff = dataObject[i - 1].top - d.bottom;
          if (diff < 0) {
            // move rect up   
            d.top += diff;
            d.bottom += diff;
          }
        }
      });
      return dataObject;
    }
  
    function adjustTops(dataObject) {
      for (var i = dataObject.length; i-- > 0;) {
        if (!(i === 0 || i === dataObject.length - 1)) {
          var diff = dataObject[i + 1].bottom - dataObject[i].top;
          if (diff > 0) {
            // move rect down
            dataObject[i].top += diff;
            dataObject[i].bottom += diff;
          }
        }
      }
      return dataObject;
    }
  
    function ydLine(isMobile, state, sel, key, question, globals, data, indexedTimepoint, indexedData) {
      var minX = data[0].timePointIndex;
      var maxX = data[data.length - 1].timePointIndex;
      var minY = d3.min(data, function (d) {
        return d.value;
      });
      var maxY = d3.max(data, function (d) {
        return d.value;
      });
      var lastPointShownAtIndex = indexedTimepoint.indexOf(question.lastPointShownAt.toString());
  
      var periods = [{ year: lastPointShownAtIndex, class: "blue", title: "" }, { year: maxX, class: "blue", title: globals.drawAreaTitle }];
      var segmentBorders = [minX].concat(periods.map(function (d) {
        return d.year;
      }));
  
      var drawAxes = function drawAxes(c) {
        c.axis.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + c.height + ")")
            .call(c.xAxis)
            .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-65)");
  
        c.axis.append("g").attr("class", "y axis").call(c.yAxis);
      };
  
      var makeLabel = function makeLabel(lowerPos, pos, addClass) {
        var x = c.x(pos);
        var y = c.y(indexedData[pos]);
        var text = formatValue(indexedData[pos], question.unit, question.precision);
  
        var label = c.labels.append("div").classed("data-label", true).classed(addClass, true).style("left", x + "px").style("top", y + "px");
        label.append("span").append("div").attr("class", "question-label update-font").text(text);
  
        if (pos == minX && isMobile) {
          label.classed("edge-left", true);
        }
        if (pos == maxX && isMobile) {
          label.classed("edge-right", true);
        }
  
        var circles = void 0;
        var counter = 0;
        for (var between = lowerPos + 1; between <= pos; between++) {
          c.dots.append("circle").attr("r", 4.5).attr("cx", c.x(between)).attr("cy", c.y(indexedData[between])).attr("class", addClass);
          counter = counter + 1;
        }
  
        circles = c.dots.selectAll("circle:nth-last-child(-n+" + counter + ")");
        /*
        return [
          c.dots.append("circle")
            .attr("r", 4.5)
            .attr("cx", x)
            .attr("cy", y)
            .attr("class", addClass),
          label
        ];
        */
        return [circles, label];
      };
  
      var drawChart = function drawChart(lower, upper, addClass) {
        var definedFn = function definedFn(d) {
          return d.year >= lower && d.year <= upper;
        };
        var area = d3.area().curve(d3.curveMonotoneX).x(ƒ("year", c.x)).y0(ƒ("value", c.y)).y1(c.height).defined(definedFn);
        var line = d3.area().curve(d3.curveMonotoneX).x(ƒ("year", c.x)).y(ƒ("value", c.y)).defined(definedFn);
  
        if (lower == minX) {
          makeLabel(minX - 1, minX, addClass);
        }
        var svgClass = addClass + (upper == lastPointShownAtIndex ? " median" : "");
  
        var group = c.charts.append("g");
        group.append("path").attr("d", area(data)).attr("class", "area " + svgClass).attr("fill", "url(#gradient-" + addClass + ")");
        group.append("path").attr("d", line(data)).attr("class", "line " + svgClass);
  
        return [group].concat(makeLabel(lower, upper, svgClass));
      };
  
      // make visual area empty
      sel.html("");
  
      var margin = {
        top: 44,
        // right: isMobile ? 20 : 50,
        right: 50,
        bottom: 30,
        // left: isMobile ? 20 : 100
        left: 100
      };
      var heightCap = 84;
      var width = sel.node().offsetWidth;
      var height = 400;
      var c = {
        width: width - (margin.left + margin.right),
        height: height - (margin.top + margin.bottom)
      };
  
      // configure scales
      var graphMinY = question.yAxisMin ? question.yAxisMin : minY >= 0 ? 0 : minY * getRandom(1, 1.5);
      var graphMaxY = question.yAxisMax ? question.yAxisMax : maxY + (maxY - graphMinY) * getRandom(0.4, 1); // add 40 - 100% for segment titles
      c.x = d3.scaleLinear().range([0, c.width]);
      c.x.domain([minX, maxX]);
      c.y = d3.scaleLinear().range([c.height, 0]);
      c.y.domain([graphMinY, graphMaxY]);
  
      c.svg = sel.append("svg").attr("width", width).attr("height", height).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")").attr("width", c.width).attr("height", c.height);
  
      // gradients
      c.defs = d3.select(c.svg.node().parentNode).append("defs");
      ["black", "red", "blue"].forEach(function (color) {
        var gradient = c.defs.append("linearGradient").attr("id", "gradient-" + color).attr("x1", "0%").attr("y1", "0%").attr("x2", "0%").attr("y2", "100%");
        gradient.append("stop").attr("offset", "0%").attr("class", "start");
        gradient.append("stop").attr("offset", "100%").attr("class", "end");
      });
  
      c.defs.append("marker").attr("id", "preview-arrowp").attr("orient", "auto").attr("viewBox", "0 0 10 10").attr("markerWidth", 6).attr("markerHeight", 6).attr("refX", 1).attr("refY", 5).append("path").attr("d", "M 0 0 L 10 5 L 0 10 z");
  
      // make background grid
      c.grid = c.svg.append("g").attr("class", "grid");
      c.grid.append("g").attr("class", "horizontal").call(d3.axisBottom(c.x).tickValues(c.x.ticks(maxX - minX)).tickFormat("").tickSize(c.height)).selectAll("line").attr("class", function (d) {
        return segmentBorders.indexOf(d) !== -1 ? "highlight" : "";
      });
  
      c.grid.append("g").attr("class", "vertical").call(d3.axisLeft(c.y).tickValues(c.y.ticks(6)).tickFormat("").tickSize(-c.width));
  
      var applyMargin = function applyMargin(sel) {
        sel.style("left", margin.left + "px").style("top", margin.top + "px").style("width", c.width + "px").style("height", c.height + "px");
      };
  
      // invisible rect for dragging to work
      var dragArea = c.svg.append("rect").attr("class", "draggable").attr("x", c.x(lastPointShownAtIndex)).attr("width", c.x(maxX) - c.x(lastPointShownAtIndex)).attr("height", c.height).attr("opacity", 0);
  
      setTimeout(function () {
        var clientRect = c.svg.node().getBoundingClientRect();
        c.top = clientRect.top + window.scrollY;
        c.bottom = clientRect.bottom + window.scrollY;
      }, 1000);
  
      c.labels = sel.append("div").attr("class", "labels").call(applyMargin);
      c.axis = c.svg.append("g");
      c.charts = c.svg.append("g");
  
      var userSel = c.svg.append("path").attr("class", "your-line");
      c.dots = c.svg.append("g").attr("class", "dots");
  
      // configure axes
      c.xAxis = d3.axisBottom().scale(c.x);
      c.xAxis.tickFormat(function (d) {
        return indexedTimepoint[d];
      }).ticks(maxX - minX);
      c.yAxis = d3.axisLeft().scale(c.y); //.tickValues(c.y.ticks(6));
      c.yAxis.tickFormat(function (d) {
        return formatValue(d, question.unit, question.precision);
      });
      drawAxes(c);
  
      c.titles = sel.append("div").attr("class", "titles").call(applyMargin).style("top", "0px");
  
      // add a preview pointer 
      var xs = c.x(lastPointShownAtIndex);
      var ys = c.y(indexedData[lastPointShownAtIndex]);
  
      var xArrowStart = ys <= 300 ? xs + 45 : xs + 70;
      var yArrowStart = ys <= 300 ? ys + 30 : ys - 30;
      var yTextStart = ys <= 300 ? c.y(indexedData[lastPointShownAtIndex]) + 30 : c.y(indexedData[lastPointShownAtIndex]) - 65;
      var xTextStart = ys <= 300 ? c.x(lastPointShownAtIndex) + 30 : c.x(lastPointShownAtIndex) + 65;
  
      c.preview = c.svg.append("path").attr("class", "controls preview-pointer").attr("marker-end", "url(#preview-arrowp)").attr("d", "M" + xArrowStart + "," + yArrowStart + " Q" + xArrowStart + "," + ys + " " + (xs + 15) + "," + ys);
  
      // add preview wave
      var arc = d3.arc().startAngle(0).endAngle(Math.PI);
  
      var nrWaves = initializeWaves(4);
      c.wave = c.svg.append("g").attr("class", "wave controls");
      c.wave.append("clipPath").attr("id", "wave-clip-" + key).append("rect").attr("width", c.width).attr("height", c.height);
  
      c.wave = c.wave.append("g").attr("clip-path", "url(#wave-clip-" + key + ")").append("g").attr("transform", "translate(" + xs + ", " + ys + ")").selectAll("path").data(nrWaves).enter().append("path").attr("class", "wave").attr("d", arc);
  
      moveWave();
      function moveWave() {
        console.log("moveWave");
        c.wave.style("opacity", .6).transition().ease(d3.easeLinear).delay(function (d, i) {
          return 1000 + i * 300;
        }).duration(4000).attrTween("d", arcTween()).style("opacity", 0).on("end", restartWave);
      }
  
      function initializeWaves(nr) {
        var nrWaves = [];
        for (var i = 0; i < nr; i++) {
          nrWaves.push({});
        }
        return nrWaves;
      }
  
      function restartWave(d, i) {
        if (i === nrWaves.length - 1) {
          // restart after last wave is finished
          var nrWaves2 = initializeWaves(4);
          c.wave = c.wave.data(nrWaves2);
          c.wave.attr("d", arc);
          moveWave();
        }
      }
  
      function arcTween() {
        return function (d) {
          if (sel.classed("drawn")) {
            c.wave.interrupt();
            console.log("waves interrupted");
            return;
          }
          var interpolate = d3.interpolate(0, 100);
          return function (t) {
            d.innerRadius = interpolate(t);
            d.outerRadius = interpolate(t) + 3;
            return arc(d);
          };
        };
      }
  
      // add preview notice
      c.controls = sel.append("div").attr("class", "controls").call(applyMargin).style("padding-left", c.x(minX) + "px");
  
      c.controls.append("span").style("left", xTextStart + "px").style("top", yTextStart + "px").append("div").attr("class", "globals-drawLine update-font").text(globals.drawLine);
  
      if (typeof question.referenceValues !== "undefined") {
        addReferenceLines(c.controls, c.svg, question.referenceValues, c);
      }
  
      // make chart
      var charts = periods.map(function (entry, key) {
        var lower = key > 0 ? periods[key - 1].year : minX;
        var upper = entry.year;
  
        // segment title
        var t = c.titles.append("span").style("left", Math.ceil(c.x(lower) + 1) + "px").style("width", Math.floor(c.x(upper) - c.x(lower) - 1) + "px");
        t.append("div").attr("class", "globals-drawAreaTitle update-font").text(entry.title);
  
        // assign prediction period to variable to use it later in interactionHandler
        if (key === 1) {
          c.predictionTitle = t;
        }
  
        return drawChart(lower, upper, entry.class);
      });
  
      var resultChart = charts[charts.length - 1][0];
      var resultClip = c.charts.append("clipPath").attr("id", "result-clip-" + key).append("rect").attr("width", c.x(lastPointShownAtIndex)).attr("height", c.height);
      var resultLabel = charts[charts.length - 1].slice(1, 3);
      resultChart.attr("clip-path", "url(#result-clip-" + key + ")").append("rect").attr("width", c.width).attr("height", c.height).attr("fill", "none");
      resultLabel.map(function (e) {
        return e.style("opacity", 0);
      });
  
      // Interactive user selection part
      var userLine = d3.line().x(ƒ("year", c.x)).y(ƒ("value", c.y)).curve(d3.curveMonotoneX);
  
      if (!state.get(key, yourData)) {
        var val = data.map(function (d) {
          return { year: d.year, value: indexedData[lastPointShownAtIndex], defined: 0 };
        }).filter(function (d) {
          if (d.year == lastPointShownAtIndex) d.defined = true;
          return d.year >= lastPointShownAtIndex;
        });
        state.set(key, "yourData", val);
      }
  
      var resultSection = d3.select(".result." + key);
  
      var drawUserLine = function drawUserLine(year) {
        userSel.attr("d", userLine.defined(ƒ("defined"))(state.get(key, yourData)));
        var d = state.get(key, yourData).filter(function (d) {
          return d.year === year;
        })[0];
        var dDefined = state.get(key, yourData).filter(function (d) {
          return d.defined && d.year !== lastPointShownAtIndex;
        });
  
        if (!d.defined) {
          return;
        }
  
        var dot = c.dots.selectAll("circle.result").data(dDefined);
        dot.enter().append("circle").merge(dot).attr("r", 4.5).attr("cx", function (de) {
          return c.x(de.year);
        }).attr("cy", function (de) {
          return c.y(de.value);
        }).attr("class", "result");
  
        var yourResult = c.labels.selectAll(".your-result").data([d]);
        yourResult.enter().append("div").classed("data-label your-result", true).classed("edge-right", isMobile).merge(yourResult).style("z-index", function () {
          return year === lastPointShownAtIndex ? 1 : 2;
        }) // should always be != , z-index=2
        .style("left", function () {
          return c.x(year) + "px";
        }).style("top", function (r) {
          return c.y(r.value) + "px";
        }).html("").append("span").append("div").attr("class", "question-label update-font").text(function (r) {
          return question.precision ? formatValue(r.value, question.unit, question.precision) : formatValue(r.value, question.unit, question.precision, 0);
        });
      };
      drawUserLine(lastPointShownAtIndex);
  
      var interactionHandler = function interactionHandler() {
        if (state.get(key, resultShown)) {
          return;
        }
  
        sel.node().classList.add("drawn");
  
        var pos = d3.mouse(c.svg.node());
        // if (pos[1] < margin.top + 4) { return; }
        if (pos[1] < 0) {
          return;
        }
        var year = clamp(lastPointShownAtIndex, maxX, c.x.invert(pos[0]));
        var value = clamp(c.y.domain()[0], c.y.domain()[1], c.y.invert(pos[1]));
        var yearPoint = lastPointShownAtIndex;
  
        state.get(key, yourData).forEach(function (d) {
          if (d.year > lastPointShownAtIndex) {
            if (Math.abs(d.year - year) < .5) {
              d.value = value;
              yearPoint = d.year;
            }
            if (d.year - year < 0.5) {
              d.defined = true;
              yearPoint = d.year;
            }
          }
        });
  
        if (pos[1] < heightCap) {
          c.predictionTitle.style("opacity", 0);
        } else if (pos[1] >= heightCap) {
          c.predictionTitle.style("opacity", 1);
        }
  
        drawUserLine(yearPoint);
        
        if (!state.get(key, completed) &&
                    (d3.min(state.get(key, yourData), ƒ("value")) <= 0)
                    || (d3.mean(state.get(key, yourData), ƒ("defined")) == 1)
        ) {
          state.set(key, completed, true);
          resultSection.node().classList.add("finished");
          resultSection.select("button").node().removeAttribute("disabled");
        }
      };
  
      c.svg.call(d3.drag().on("drag", interactionHandler));
      c.svg.on("click", interactionHandler);
  
      var showResultChart = function showResultChart() {
        if (!state.get(key, completed)) {
          return;
        }
        c.labels.selectAll(".your-result").node().classList.add("hideLabels");
        resultClip.transition().duration(700).attr("width", c.x(maxX));
        dragArea.attr("class", "");
        resultLabel[0].transition().duration(30).delay(function (d, i) {
          return (i + 1) / resultLabel[0].size() * 700;
        }).style("opacity", 1);
  
        setTimeout(function () {
          resultLabel.map(function (e) {
            return e.style("opacity", 1);
          });
          resultSection.node().classList.add("shown");
  
          if (!state.get(key, score) && globals.showScore) {
            var truth$$1 = data.filter(function (d) {
              return d.year > lastPointShownAtIndex;
            });
            getScore(key, truth$$1, state, graphMaxY, graphMinY, resultSection, globals.scoreTitle, globals.scoreButtonText, globals.scoreButtonTooltip, globals.scoreHtml);
          }
          state.set(key, resultShown, true);
        }, 700);
      };
      resultSection.select("button").on("click", showResultChart);
      if (state.get(key, resultShown)) {
        showResultChart();
      }
    }
  
    function ydBar(isMobile, state, sel, key, question, globals, data, indexedTimepoint, indexedData) {
      var minX = data[0].timePointIndex;
      var maxX = data[data.length - 1].timePointIndex;
      var minY = d3.min(data, function (d) {
        return d.value;
      });
      var maxY = d3.max(data, function (d) {
        return d.value;
      });
      var lastPointShownAtIndex = indexedTimepoint.indexOf(question.lastPointShownAt.toString());
  
      var drawAxes = function drawAxes(c) {
        c.axis.append("g").attr("class", "x axis").attr("transform", "translate(0," + c.height + ")");
        // .call(c.xAxis);
  
        c.axis.append("g").attr("class", "y axis").call(c.yAxis);
      };
  
      var makeLabel = function makeLabel(pos, addClass) {
        var x = c.x(truth) + c.x.bandwidth() / 2;
        var truthValue = data[0].value;
        var y = c.y(truthValue);
  
        var text = formatValue(truthValue, question.unit, question.precision);
  
        var label = c.labels.append("div").classed("data-label", true).classed(addClass, true).style("opacity", 0).style("left", x + "px").style("top", y + "px");
        label.append("span")
        // .classed("no-dot question-label update-font", true)
        .classed("no-dot", true).append("div").classed("question-label update-font", true).text(text);
  
        if (pos == minX && isMobile) {
          label.classed("edge-left", true);
        }
        if (pos == maxX && isMobile) {
          label.classed("edge-right", true);
        }
  
        return [{}, label];
      };
  
      var drawChart = function drawChart(addClass) {
        var group = c.charts.append("g").attr("class", "truth");
  
        makeLabel(truth, addClass);
  
        var truthSelection = group.append("rect").attr("class", "bar").attr("x", c.x(truth)).attr("y", c.height).attr("height", 0).attr("width", c.x.bandwidth());
        return truthSelection;
      };
  
      // make visual area empty
      sel.html("");
  
      var margin = {
        top: 40,
        // right: isMobile ? 20 : 50,
        right: 50,
        bottom: 30,
        // left: isMobile ? 20 : 100
        left: 100
      };
      var width = sel.node().offsetWidth;
      var height = 400;
      var c = {
        width: width - (margin.left + margin.right),
        height: height - (margin.top + margin.bottom)
      };
  
      var graphMinY = question.yAxisMin ? question.yAxisMin : minY >= 0 ? 0 : minY * getRandom(1, 1.5);
      var graphMaxY = question.yAxisMax ? question.yAxisMax : maxY + (maxY - graphMinY) * getRandom(0.4, 1); // add 40 - 100% for segment titles
      c.x = d3.scaleBand().rangeRound([0, c.width]).padding(0.1);
      c.x.domain([prediction, truth]);
      c.y = d3.scaleLinear().range([c.height, 0]);
      c.y.domain([graphMinY, graphMaxY]);
  
      c.svg = sel.append("svg").attr("width", width).attr("height", height).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")").attr("width", c.width).attr("height", c.height);
  
      // gradients
      c.defs = d3.select(c.svg.node().parentNode).append("defs");
      ["black", "red", "blue"].forEach(function (color) {
        var gradient = c.defs.append("linearGradient").attr("id", "gradient-" + color).attr("x1", "0%").attr("y1", "0%").attr("x2", "0%").attr("y2", "100%");
        gradient.append("stop").attr("offset", "0%").attr("class", "start");
        gradient.append("stop").attr("offset", "100%").attr("class", "end");
      });
  
      c.defs.append("marker").attr("id", "preview-arrowp").attr("orient", "auto").attr("viewBox", "0 0 10 10").attr("markerWidth", 6).attr("markerHeight", 6).attr("refX", 1).attr("refY", 5).append("path").attr("d", "M 0 0 L 10 5 L 0 10 z");
  
      // make background grid
      c.grid = c.svg.append("g").attr("class", "grid");
  
      c.grid.append("g").attr("class", "vertical").call(d3.axisLeft(c.y).tickValues(c.y.ticks(6)).tickFormat("").tickSize(-c.width));
  
      var applyMargin = function applyMargin(sel) {
        sel.style("left", margin.left + "px").style("top", margin.top + "px").style("width", c.width + "px").style("height", c.height + "px");
      };
  
      setTimeout(function () {
        var clientRect = c.svg.node().getBoundingClientRect();
        c.top = clientRect.top + window.scrollY;
        c.bottom = clientRect.bottom + window.scrollY;
      }, 1000);
  
      c.labels = sel.append("div").attr("class", "labels").call(applyMargin);
      c.axis = c.svg.append("g");
      c.charts = c.svg.append("g").attr("class", "charts");
      c.xPredictionCenter = c.x(prediction) + c.x.bandwidth() / 2;
  
      var userSel = c.svg.append("rect").attr("class", "your-rect");
  
      // invisible rect for dragging to work
      var dragArea = c.svg.append("rect").attr("class", "draggable").attr("x", c.x(prediction)).attr("width", c.x.bandwidth()).attr("height", c.height).attr("opacity", 0);
  
      // configure axes
      c.xAxis = d3.axisBottom().scale(c.x);     
      c.yAxis = d3.axisLeft().scale(c.y).tickValues(c.y.ticks(6));
      c.yAxis.tickFormat(function (d) {
        return formatValue(d, question.unit, question.precision);
      });
      drawAxes(c);
  
      c.titles = sel.append("div").attr("class", "titles").call(applyMargin).style("top", "0px");
  
      // add a preview pointer 
      var xs = c.xPredictionCenter;
      var ys = c.height - 30;
      var xArrowStart = xs + 45;
      var yArrowStart = ys - 50;
      var xTextStart = xArrowStart + 5;
      var yTextStart = yArrowStart - 10;
  
      c.preview = c.svg.append("path").attr("class", "controls preview-pointer").attr("marker-end", "url(#preview-arrowp)").attr("d", "M" + xArrowStart + "," + yArrowStart + " Q" + xs + "," + yArrowStart + " " + xs + "," + (ys - 10));
  
      // add preview wave
      var arc = d3.arc().startAngle(0).endAngle(2 * Math.PI);
  
      var nrWaves = initializeWaves(4);
      c.wave = c.svg.append("g").attr("class", "wave controls");
      c.wave.append("clipPath").attr("id", "wave-clip-" + key).append("rect").attr("width", c.width).attr("height", c.height);
  
      c.wave = c.wave.append("g").attr("clip-path", "url(#wave-clip-" + key + ")").append("g").attr("transform", "translate(" + xs + ", " + ys + ")").selectAll("path").data(nrWaves).enter().append("path").attr("class", "wave").attr("d", arc);
  
      moveWave();
      function moveWave() {
        c.wave.style("opacity", .6).transition().ease(d3.easeLinear).delay(function (d, i) {
          return 1000 + i * 300;
        }).duration(4000).attrTween("d", arcTween()).style("opacity", 0).on("end", restartWave);
      }
  
      function initializeWaves(nr) {
        var nrWaves = [];
        for (var i = 0; i < nr; i++) {
          nrWaves.push({});
        }
        return nrWaves;
      }
  
      function restartWave(d, i) {
        if (i === nrWaves.length - 1) {
          // restart after last wave is finished
          var nrWaves2 = initializeWaves(4);
          c.wave = c.wave.data(nrWaves2);
          c.wave.attr("d", arc);
          moveWave();
        }
      }
  
      function arcTween() {
        return function (d) {
          if (sel.classed("drawn")) {
            c.wave.interrupt();
            console.log("waves interrupted");
            return;
          }
          var interpolate = d3.interpolate(0, 100);
          return function (t) {
            d.innerRadius = interpolate(t);
            d.outerRadius = interpolate(t) + 3;
            return arc(d);
          };
        };
      }
  
      // add preview notice
      c.controls = sel.append("div").attr("class", "controls").call(applyMargin).style("padding-left", c.xPredictionCenter);
  
      c.controls.append("span").style("left", xTextStart + "px").style("top", yTextStart + "px").append("div").attr("class", "globals-drawBar update-font").text(globals.drawBar);
  
      if (typeof question.referenceValues !== "undefined") {
        if (question.referenceShape === "tick") {
          addReferenceValues(c.controls, c.svg, question.referenceValues, c, false);
        } else {
          //question.referenceShape === "line"
          addReferenceValues(c.controls, c.svg, question.referenceValues, c, true);
        }
      }
  
      // make chart
      var truthSelection = drawChart("blue");
  
      // segment title
      c.predictionTitle = c.titles.append("span").style("left", "1px").style("width", c.width / 2 - 1 + "px");
      c.predictionTitle.append("div").attr("class", "globals-drawAreaTitle update-font").text(globals.drawAreaTitle);
  
      // Interactive user selection part
      userSel.attr("x", c.x(prediction)).attr("y", c.height - 30).attr("width", c.x.bandwidth()).attr("height", 30);
  
      if (!state.get(key, yourData)) {
        var val = data.map(function (d) {
          return { year: d.year, value: indexedData[lastPointShownAtIndex], defined: 0 };
        }).filter(function (d) {
          if (d.year == lastPointShownAtIndex) d.defined = true;
          return d.year >= lastPointShownAtIndex;
        });
        state.set(key, "yourData", val);
      }
  
      var resultSection = d3.select(".result." + key);
      var drawUserBar = function drawUserBar(year) {
        var h = c.y(state.get(key, yourData)[0].value);
        userSel.attr("y", h).attr("height", c.height - h);
        var d = state.get(key, yourData).filter(function (d) {
          return d.year === year;
        })[0];
        // const dDefined = state.get(key, yourData).filter(d => d.defined && (d.year !== lastPointShownAtIndex));
  
        if (!d.defined) {
          return;
        }
  
        var yourResult = c.labels.selectAll(".your-result").data([d]);
        yourResult.enter().append("div").classed("data-label your-result", true).classed("edge-right", isMobile).merge(yourResult).style("left", c.xPredictionCenter + "px").style("top", function (r) {
          return c.y(r.value) + "px";
        }).html("").append("span").classed("no-dot", true).append("div").classed("question-label update-font", true).text(function (r) {
          return question.precision ? formatValue(r.value, question.unit, question.precision) : formatValue(r.value, question.unit, question.precision, 0);
        });
      };
      if (sel.classed("drawn")) {
        drawUserBar(lastPointShownAtIndex);
      }
  
      var interactionHandler = function interactionHandler() {
        if (state.get(key, resultShown)) {
          return;
        }
  
        sel.node().classList.add("drawn");
  
        var pos = d3.mouse(c.svg.node());
        // if (pos[1] < margin.top) { return; }
        if (pos[1] < 0) {
          return;
        }
        var value = clamp(c.y.domain()[0], c.y.domain()[1], c.y.invert(pos[1]));
        var yearPoint = lastPointShownAtIndex;
  
        state.get(key, yourData).forEach(function (d) {
          d.value = value;
          d.defined = true;
          yearPoint = d.year;
        });
  
        if (pos[1] < 80) {
          c.predictionTitle.style("opacity", 0);
        } else if (pos[1] >= 80) {
          c.predictionTitle.style("opacity", 1);
        }
  
        drawUserBar(yearPoint);
  
        if (!state.get(key, completed) && d3.mean(state.get(key, yourData), ƒ("defined")) == 1) {
          state.set(key, completed, true);
          resultSection.node().classList.add("finished");
          resultSection.select("button").node().removeAttribute("disabled");
        }
      };
  
      c.svg.call(d3.drag().on("drag", interactionHandler));
      c.svg.on("click", interactionHandler);
  
      var showResultChart = function showResultChart() {
        if (!state.get(key, completed)) {
          return;
        }
        c.labels.selectAll(".your-result").node().classList.add("hideLabels");
  
        var h = c.y(data[0].value);
        truthSelection.transition().duration(1300).attr("y", h).attr("height", c.height - h);
  
        dragArea.attr("class", "");
  
        setTimeout(function () {
          c.labels.select("div.data-label").style("opacity", 1);
          resultSection.node().classList.add("shown");
  
          if (!state.get(key, score) && globals.showScore) {
            var _truth = data.filter(function (d) {
              return d.year === lastPointShownAtIndex;
            });
            getScore(key, _truth, state, graphMaxY, graphMinY, resultSection, globals.scoreTitle, globals.scoreButtonText, globals.scoreButtonTooltip, globals.scoreHtml);
          }
          state.set(key, resultShown, true);
        }, 1300);
      };
      resultSection.select("button").on("click", showResultChart);
      if (state.get(key, resultShown)) {
        showResultChart();
      }
    }
  
    /*
    import { ƒ } from "./helpers/function";
    import { formatValue } from "./helpers/formatValue";
    import { clamp } from "./helpers/clamp";
    import { getRandom } from "./helpers/getRandom";
    import { yourData, resultShown, completed, score, prediction, truth } from "./helpers/constants";
    import { getScore } from "./results/score";
    import { addReferenceValues } from "./helpers/referenceValues";
    */
  
    function ydCheckbox(isMobile, state, sel, key, question, globals, data) {
  
      sel.html("");
      var selDiv = sel.append("div");
      var selLabel = void 0;
      var prediction$$1 = [];
      var cb = void 0;
  
      data.forEach(function (ele, i) {
        selLabel = selDiv.append("label").attr("class", "question-multipleChoice update-font answer-container l-" + i).html(ele.timePoint);
  
        // checkbox for answers
        selLabel.append("span").attr("class", "answer-checkmark-truth t-" + i).append("div").attr("class", "input");
  
        // checkbox for guesses
        cb = selLabel.append("input").attr("type", "checkbox").attr("name", "cb").attr("value", "v" + i).on("click", handleClick);
  
        selLabel.append("span").attr("class", "answer-checkmark");
  
        // preset the checkboxes with the guesses already made for resize event
        prediction$$1[i] = state.get(key, yourData) ? state.get(key, yourData)[i] : false;
        cb.node().checked = prediction$$1[i];
      });
  
      var resultSection = d3.select(".result." + key);
      resultSection.select("button").on("click", showResultChart);
  
      if (state.get(key, resultShown)) {
        showResultChart();
      }
  
      function handleClick() {
        if (state.get(key, resultShown)) {
          return;
        }
        var index = d3.select(this).attr("value").substring(1);
        console.log("Clicked, new value [" + index + "] = " + d3.select(this).node().checked);
        prediction$$1[index] = d3.select(this).node().checked;
        state.set(key, yourData, prediction$$1);
        resultSection.node().classList.add("finished");
        resultSection.select("button").node().removeAttribute("disabled");
      }
  
      function showResultChart() {
        state.set(key, completed, true);
        // disable hovers
        var css = ".answer-container:hover input ~ .answer-checkmark { background-color: #eee;}";
        css = css + " .answer-container input:checked ~ .answer-checkmark { background-color: orange;}";
        var style = document.createElement("style");
  
        if (style.styleSheet) {
          style.styleSheet.cssText = css;
        } else {
          style.appendChild(document.createTextNode(css));
        }
        document.getElementsByTagName("head")[0].appendChild(style);
  
        // disable checkboxes
        sel.selectAll("div input").each(function () {
          d3.select(this).node().disabled = true;
        });
        // display result (with transition)
        var correctAnswers = 0;
        data.forEach(function (ele, i) {
          if (ele.value === prediction$$1[i]) {
            correctAnswers = correctAnswers + 1;
          }
          sel.select("div span.answer-checkmark-truth.t-" + i).classed("checked", ele.value).style("background-color", "#fff").transition().ease(ele.value ? d3.easeExpIn : d3.easeLinear).duration(100).delay(i * 100).style("background-color", ele.value ? "#00345e" : "#eee");
  
          sel.select("div span.answer-checkmark-truth.t-" + i + " div.input").classed("checked", ele.value);
  
          sel.select("div .answer-container.l-" + i).transition().duration(100).delay(i * 100).style("color", ele.value ? "#00345e" : "#eee");
        });
  
        // call getScore 
        var durationTrans = 100 * (data.length + 1);
        setTimeout(function () {
          resultSection.node().classList.add("shown");
          if (!state.get(key, score) && globals.showScore) {
            var myScore = Math.round(correctAnswers / prediction$$1.length * 100);
            console.log("score: " + myScore);
            state.set(key, score, myScore);
            getFinalScore(key, state, resultSection, globals.scoreTitle, globals.scoreButtonText, globals.scoreButtonTooltip, globals.scoreHtml);
          }
          state.set(key, resultShown, true);
        }, durationTrans);
      }
    }
  
    function myState () {
      var state = {};
      stateAPI();
  
      function stateAPI() {
        state = {};
      }
  
      stateAPI.setQuestion = function (question) {
        if (!state[question]) {
          state[question] = {};
        }
      };
  
      stateAPI.getQuestion = function (question) {
        return state[question];
      };
  
      stateAPI.getAllQuestions = function () {
        return Object.keys(state);
      };
  
      stateAPI.getState = function () {
        return state;
      };
  
      stateAPI.set = function (question, key, value) {
        if (!state[question][key]) {
          state[question][key] = {};
        }
        state[question][key] = value;
      };
  
      stateAPI.get = function (question, key) {
        return state[question][key];
      };
  
      // for calculating the score
      stateAPI.getResult = function (question, key) {
        var oldArray = state[question][key];
        // remove first element for line charts, which was not a prediction but the starting point for the line
        var newArray = oldArray.length > 1 ? oldArray.slice(1) : oldArray;
        return newArray;
      };
  
      return stateAPI;
    }
  
    var globals = {};
  
    function youdrawit(_globals, questions) {
      var isMobile = window.innerWidth < 760;
      globals = _globals;
      var state = myState();
  
      var drawGraphs = function drawGraphs() {
        d3.selectAll(".you-draw-it").each(function (d, i) {
          var sel = d3.select(this);
          var question = questions[i];
          var key = question.key;
          var originalData = question.data;
  
          var data = originalData.map(function (ele, index) {
            return {
              year: index,
              timePointIndex: index,
              timePoint: Object.keys(ele)[0],
              value: ele[Object.keys(ele)[0]]
            };
          });
  
          var indexedTimepoint = data.map(function (ele) {
            return ele.timePoint;
          });
          var indexedData = data.map(function (ele) {
            return ele.value;
          });
  
          state.setQuestion(key);
  
          if (data.length < 1) {
            console.log("No data available for:", key);
            return;
          }
  
          if (question.chartType === "barChart") {
            ydBar(isMobile, state, sel, key, question, globals, data, indexedTimepoint, indexedData);
          } else if (question.chartType === "timeSeries") {
            ydLine(isMobile, state, sel, key, question, globals, data, indexedTimepoint, indexedData);
          } else if (question.chartType === "multipleChoice") {
            ydCheckbox(isMobile, state, sel, key, question, globals, data);
          }
        });
      };
  
      document.addEventListener("DOMContentLoaded", drawGraphs);
  
      window.addEventListener("resize", debounce(function () {
        drawGraphs();
      }, 500));
    }
  
    function getLanguage() {
      return globals.default;
    }
  
    function _interface () {
  
      var options = {};
      options.containerDiv = d3.select("body");
      options.globals = {};
      /* option.globals contain:
        g.default
        g.header
        g.subHeader
        g.drawAreaTitle
        g.drawLine
        g.drawBar
        g.resultButtonText
        g.resultButtonTooltip
        g.showScore
        g.scoreTitle
        g.scoreButtonText
        g.scoreButtonTooltip
        g.scoreHtml
      */
      options.questions = [];
      /* options.questions is an array of question objects q with:
        q.data
        q.heading
        q.subHeading
        q.resultHtml
        q.unit
        q.precision
        q.lastPointShownAt
        q.yAxisMin
        q.yAxisMax
        q.referenceValues
        q.referenceShape
          // the following are internal properties
        q.chartType
        q.key
      */
  
      // API for external access
      function chartAPI(selection) {
        selection.each(function () {
          options.containerDiv = d3.select(this);
          if (!options.questions) {
            console.log("no questions specified!");
          }
          if (Object.keys(options.globals).length === 0) {
            setGlobalDefault("English");
          }
          completeQuestions();
          completeDOM();
          youdrawit(options.globals, options.questions);
        });
        return chartAPI;
      }
  
      chartAPI.questions = function (_) {
        if (!arguments.length) return options.questions;
        options.questions = _;
        return chartAPI;
      };
  
      chartAPI.globals = function (_) {
        if (!arguments.length) return options.globals;
        for (var key in _) {
          if (_.hasOwnProperty(key)) {
            options.globals[key] = _[key];
            if (key === "default") {
              setGlobalDefault(_[key]);
            }
          }
        }
        return chartAPI;
      };
  
      function setGlobalDefault(lang) {
        var g = options.globals;
        g.showScore = typeof g.showScore === "undefined" ? true : g.showScore;
        if (lang === "de") {
          // de (German)
          g.resultButtonText = typeof g.resultButtonText === "undefined" ? "Zeig mir die Lösung!" : g.resultButtonText;
          g.resultButtonTooltip = typeof g.resultButtonTooltip === "undefined" ? "Zeichnen Sie Ihre Einschätzung. Der Klick verrät, ob sie stimmt." : g.resultButtonTooltip;
          g.scoreTitle = typeof g.scoreTitle === "undefined" ? "Ihr Ergebnis:" : g.scoreTitle;
          g.scoreButtonText = typeof g.scoreButtonText === "undefined" ? "Zeig mir, wie gut ich war!" : g.scoreButtonText;
          g.scoreButtonTooltip = typeof g.scoreButtonTooltip === "undefined" ? "Klicken Sie hier, um Ihr Gesamtergebnis zu sehen" : g.scoreButtonTooltip;
          g.drawAreaTitle = typeof g.drawAreaTitle === "undefined" ? "Ihre\nEinschätzung" : g.drawAreaTitle;
          g.drawLine = typeof g.drawLine === "undefined" ? "Zeichnen Sie von hier\nden Verlauf zu Ende" : g.drawLine;
          g.drawBar = typeof g.drawBar === "undefined" ? "Ziehen Sie den Balken\nauf die entsprechende Höhe" : g.drawBar;
        } else if (lang === "fr") {
          // fr (French)
          g.default = "fr";
          g.resultButtonText = typeof g.resultButtonText === "undefined" ? "Montrez-moi le résultat" : g.resultButtonText;
          g.resultButtonTooltip = typeof g.resultButtonTooltip === "undefined" ? "A vous de dessiner la courbe. Pour voir la bonne réponse, cliquez ici" : g.resultButtonTooltip;
          g.scoreTitle = typeof g.scoreTitle === "undefined" ? "Votre résultat:" : g.scoreTitle;
          g.scoreButtonText = typeof g.scoreButtonText === "undefined" ? "Montrez-moi la bonne réponse" : g.scoreButtonText;
          g.scoreButtonTooltip = typeof g.scoreButtonTooltip === "undefined" ? "Cliquez ici pour obtenir des explications" : g.scoreButtonTooltip;
          g.drawAreaTitle = typeof g.drawAreaTitle === "undefined" ? "Votre\nsupposition" : g.drawAreaTitle;
          g.drawLine = typeof g.drawLine === "undefined" ? "Placez votre doigt\nou votre souris ici\net dessinez la courbe" : g.drawLine;
          g.drawBar = typeof g.drawBar === "undefined" ? "Montez la barre\njusqu’à la hauteur supposée" : g.drawBar;
        } else {
          // lang === "en" (English)
          g.default = "en";
          g.resultButtonText = typeof g.resultButtonText === "undefined" ? "Show me the result!" : g.resultButtonText;
          g.resultButtonTooltip = typeof g.resultButtonTooltip === "undefined" ? "Draw your guess. Upon clicking here, you see if you're right." : g.resultButtonTooltip;
          g.scoreTitle = typeof g.scoreTitle === "undefined" ? "Your result:" : g.scoreTitle;
          g.scoreButtonText = typeof g.scoreButtonText === "undefined" ? "Show me how good I am!" : g.scoreButtonText;
          g.scoreButtonTooltip = typeof g.scoreButtonTooltip === "undefined" ? "Click here to see your result" : g.scoreButtonTooltip;
          g.drawAreaTitle = typeof g.drawAreaTitle === "undefined" ? "Your\nguess" : g.drawAreaTitle;
          g.drawLine = typeof g.drawLine === "undefined" ? "draw the graph\nfrom here to the end" : g.drawLine;
          g.drawBar = typeof g.drawBar === "undefined" ? "drag the bar\nto the estimated height" : g.drawBar;
        }
      }
  
      function completeQuestions() {
        if (typeof options.globals.scoreHtml !== "undefined") {
          if (typeof options.globals.scoreHtml === "string" || options.globals.scoreHtml instanceof String) {
            if (!checkResult(options.globals.scoreHtml)) {
              console.log("invalid scoreHtml!");
              options.globals.scoreHtml = void 0; // set to undefined
            } else {
              options.globals.scoreHtml = [{ lower: 0, upper: 101, html: options.globals.scoreHtml }];
            }
          } else {
            // options.globals.scoreHtml is an array
            if (typeof options.globals.scoreHtml.length !== "undefined") {
              options.globals.scoreHtml.forEach(function (range) {
                var exp = range.html;
                if (!checkResult(exp)) {
                  console.log("invalid scoreHtml! -> set to empty string");
                  range.html = "";
                }
              });
            }
          }
        }
  
        options.questions.forEach(function (q, index) {
          if (!q.data) {
            console.log("no data specified!");
          }
          if (!checkResult(q.resultHtml)) {
            console.log("invalid result!");
          }
  
          q.chartType = getChartType(q.data);
          q.heading = typeof q.heading === "undefined" ? "" : q.heading;
          q.subHeading = typeof q.subHeading === "undefined" ? "" : q.subHeading;
          q.resultHtml = typeof q.resultHtml === "undefined" ? "<br>" : q.resultHtml;
          q.unit = typeof q.unit === "undefined" ? "" : q.unit;
          q.precision = typeof q.precision === "undefined" ? 1 : q.precision;
          q.referenceShape = typeof q.referenceShape === "undefined" ? "line" : q.referenceShape;
          q.key = "q" + (index + 1);
  
          if (q.chartType === "barChart") {
            q.data = [{ value: q.data }];
          }
  
          if (!q.lastPointShownAt) {
            if (q.chartType === "timeSeries") {
              var nextToLast = q.data[q.data.length - 2];
              q.lastPointShownAt = Object.keys(nextToLast)[0];
            } else if (q.chartType === "barChart") {
              var onlyElement = q.data[0];
              q.lastPointShownAt = Object.keys(onlyElement)[0];
            }
          }
          console.log("display question " + index + " as " + q.chartType);
        });
      }
  
      function getChartType(data) {
        var chartType = void 0;
        if (isNumber(data)) {
          chartType = "barChart";
        } else {
          var firstObj = data[0];
          var num = true;
          for (var key in firstObj) {
            if (firstObj.hasOwnProperty(key)) {
              num = num && isNumber(firstObj[key]);
            }
          }
          chartType = num ? "timeSeries" : "multipleChoice";
        }
        return chartType;
      }
  
      function isNumber(n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
      }
  
      function completeDOM() {
        var art = options.containerDiv.append("article").attr("id", "content").attr("class", "container");
  
        var intro = art.append("div").attr("class", "intro");
        intro.append("h1").append("div").attr("class", "globals-header update-font").html(options.globals.header);
        intro.append("p").append("div").attr("class", "globals-subHeader update-font").html(options.globals.subHeader);
  
        var questions = art.append("div").attr("class", "questions");
  
        options.questions.forEach(function (q) {
          var question = questions.append("div").attr("class", "question");
          question.append("h2").append("div").attr("class", "question-heading update-font").html(q.heading);
          question.append("h3").append("div").attr("class", "question-subHeading update-font").html(q.subHeading);
          question.append("div").attr("class", "you-draw-it " + q.key).attr("data-key", q.key);
  
          var res = question.append("div").attr("class", "result " + q.key);
          var ac = res.append("div").attr("class", "actionContainer");
          ac.append("button").attr("class", "showAction").attr("disabled", "disabled").append("div").attr("class", "globals-resultButtonText update-font").text(options.globals.resultButtonText);
          ac.append("div").attr("class", "tooltipcontainer").append("span").attr("class", "tooltiptext globals-resultButtonTooltip update-font").text(options.globals.resultButtonTooltip);
  
          res.append("div").attr("class", "text").append("p").append("div").attr("class", "question-resultHtml update-font").html(q.resultHtml);
        });
      }
  
      function checkResult(exp) {
        // checks if html might contain javascript
        if (!exp) {
          return true;
        }
        var expUC = exp.toUpperCase();
        if (expUC.indexOf("<") !== -1 && expUC.indexOf("SCRIPT") !== -1 && expUC.indexOf(">") !== -1) {
          console.log("--- invalid html!");
          console.log("--- expression was: ");
          console.log(exp);
          return false;
        } else {
          return true;
        }
      }
  
      return chartAPI;
    }
  
    exports.chart = _interface;
  
    Object.defineProperty(exports, '__esModule', { value: true });
  
  })));