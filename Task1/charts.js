// Tracking which dashboard is loaded so that multiple dashboards are not loaded multiple times
const loadedDashboards = {
  room1: false,
  room2: false,
  freezer: false,
  incubator: false,
  planer: false,
  weight_n2: false
};

function showDashboard(sectionId) {
  document.querySelectorAll('.dashboard-section').forEach(sec => {
    sec.style.display = 'none';
  });
  
  document.getElementById(sectionId).style.display = 'block';

  if (!loadedDashboards[sectionId]) {
    loadedDashboards[sectionId] = true; 
    loadAndRenderAll(sectionId);
  }
}

// Shows room1 dashboard by default
window.onload = () => {
  showDashboard('room1');
};

// Tooltip
const tooltip = d3.select("#globalTooltip");

function showTooltip(event, content) {
  tooltip.transition().duration(200).style("opacity", 0.9);
  tooltip.html(content)
         .style("left", (event.pageX + 10) + "px")
         .style("top", (event.pageY - 28) + "px");
}

function hideTooltip() {
  tooltip.transition().duration(500).style("opacity", 0);
}

// median
function median(values) {
  const sorted = values.slice().sort(d3.ascending);
  const mid = Math.floor(sorted.length / 2);
  return values.length % 2
    ? sorted[mid]
    : (sorted[mid - 1] + sorted[mid]) / 2;
}

// Pearson correlation
function pearsonCorrelation(x, y) {
  const meanX = d3.mean(x), meanY = d3.mean(y);
  const numerator = d3.sum(x.map((val, i) => (val - meanX) * (y[i] - meanY)));
  const denominator = Math.sqrt(
    d3.sum(x.map(val => (val - meanX) ** 2)) *
    d3.sum(y.map(val => (val - meanY) ** 2))
  );
  return numerator / denominator;
}

//function to draw lines and circles for mean and median
function drawLinesAndCircles(g, data, xScale, yScale, xAccessor, meanAccessor, medianAccessor, xLabel, variable) {
 
  const lineMean = d3.line()
    .x(d => xScale(xAccessor(d)))
    .y(d => yScale(meanAccessor(d)));
    
  const lineMedian = d3.line()
    .x(d => xScale(xAccessor(d)))
    .y(d => yScale(medianAccessor(d)));
    
  // mean line
  g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", lineMean);
    
  // median line
  g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "orange")
    .attr("stroke-width", 2)
    .attr("d", lineMedian);
    
  // mean circles
  g.selectAll(".mean-circle")
    .data(data)
    .enter().append("circle")
    .attr("class", "mean-circle")
    .attr("cx", d => xScale(xAccessor(d)))
    .attr("cy", d => yScale(meanAccessor(d)))
    .attr("r", 4)
    .attr("fill", "steelblue")
    .on("mouseover", (event, d) => {
      showTooltip(event, `${xLabel}: ${xAccessor(d)}<br>Mean ${variable.toUpperCase()}: ${meanAccessor(d).toFixed(2)}`);
    })
    .on("mouseout", hideTooltip);
    
  // median circles
  g.selectAll(".median-circle")
    .data(data)
    .enter().append("circle")
    .attr("class", "median-circle")
    .attr("cx", d => xScale(xAccessor(d)))
    .attr("cy", d => yScale(medianAccessor(d)))
    .attr("r", 4)
    .attr("fill", "orange")
    .on("mouseover", (event, d) => {
      showTooltip(event, `${xLabel}: ${xAccessor(d)}<br>Median ${variable.toUpperCase()}: ${medianAccessor(d).toFixed(2)}`);
    })
    .on("mouseout", hideTooltip);
}

// hourly variation
function drawHourlyChart(containerSelector, yearData, variable, year) {
  const grouped = Array.from(
    d3.group(yearData, d => d.hour),
    ([hr, vals]) => ({
      hour: +hr,
      meanVal: d3.mean(vals, d => d[variable]),
      medianVal: median(vals.map(d => d[variable]))
    })
  ).sort((a, b) => d3.ascending(a.hour, b.hour));

  const container = d3.select(containerSelector)
    .append("div")
    .attr("class", "chart-container");

  container.append("div")
    .attr("class", "chart-title")
    .text(`Hourly Variation - ${variable.toUpperCase()} - Year ${year}`);

  const svgWidth = 800, svgHeight = 400;
  const margin = { top: 20, right: 30, bottom: 50, left: 60 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const x = d3.scaleLinear()
    .domain([0, 23])
    .range([0, width]);
  g.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).ticks(24))
    .append("text")
    .attr("x", width / 2)
    .attr("y", 40)
    .attr("fill", "#000")
    .attr("text-anchor", "middle")
    .attr("class", "axis-label")
    .text("Hour");

  const minVal = d3.min(grouped, d => Math.min(d.meanVal, d.medianVal));
  const maxVal = d3.max(grouped, d => Math.max(d.meanVal, d.medianVal));
  const y = d3.scaleLinear()
    .domain([minVal, maxVal])
    .nice()
    .range([height, 0]);
  g.append("g")
    .call(d3.axisLeft(y))
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -45)
    .attr("fill", "#000")
    .attr("text-anchor", "middle")
    .attr("class", "axis-label")
    .text(variable.toUpperCase());

  drawLinesAndCircles(g, grouped, x, y, d => d.hour, d => d.meanVal, d => d.medianVal, "Hour", variable);
}

// weekly variation
function drawWeeklyChart(containerSelector, yearData, variable, year) {
  const grouped = Array.from(
    d3.group(yearData, d => d.weekday),
    ([wd, vals]) => ({
      weekday: +wd,
      meanVal: d3.mean(vals, d => d[variable]),
      medianVal: median(vals.map(d => d[variable]))
    })
  ).sort((a, b) => d3.ascending(a.weekday, b.weekday));

  const weekdayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  const container = d3.select(containerSelector)
    .append("div")
    .attr("class", "chart-container");

  container.append("div")
    .attr("class", "chart-title")
    .text(`Weekly Variation - ${variable.toUpperCase()} - Year ${year}`);

  const svgWidth = 800, svgHeight = 400;
  const margin = { top: 20, right: 30, bottom: 50, left: 60 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const x = d3.scaleLinear()
    .domain([0, 6])
    .range([0, width]);
  g.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).ticks(7).tickFormat(d => weekdayNames[d]))
    .append("text")
    .attr("x", width / 2)
    .attr("y", 40)
    .attr("fill", "#000")
    .attr("text-anchor", "middle")
    .attr("class", "axis-label")
    .text("Weekday");

  const minVal = d3.min(grouped, d => Math.min(d.meanVal, d.medianVal));
  const maxVal = d3.max(grouped, d => Math.max(d.meanVal, d.medianVal));
  const y = d3.scaleLinear()
    .domain([minVal, maxVal])
    .nice()
    .range([height, 0]);
  g.append("g")
    .call(d3.axisLeft(y))
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -45)
    .attr("fill", "#000")
    .attr("text-anchor", "middle")
    .attr("class", "axis-label")
    .text(variable.toUpperCase());

  drawLinesAndCircles(g, grouped, x, y, d => d.weekday, d => d.meanVal, d => d.medianVal, "Weekday", variable);
}

// monthly variation
function drawMonthlyChart(containerSelector, yearData, variable, year) {
  const grouped = Array.from(
    d3.group(yearData, d => d.month),
    ([m, vals]) => ({
      month: +m,
      meanVal: d3.mean(vals, d => d[variable]),
      medianVal: median(vals.map(d => d[variable]))
    })
  ).sort((a, b) => d3.ascending(a.month, b.month));

  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  const container = d3.select(containerSelector)
    .append("div")
    .attr("class", "chart-container");

  container.append("div")
    .attr("class", "chart-title")
    .text(`Monthly Variation - ${variable.toUpperCase()} - Year ${year}`);

  const svgWidth = 800, svgHeight = 400;
  const margin = { top: 20, right: 30, bottom: 50, left: 60 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const x = d3.scaleLinear()
    .domain([1, 12])
    .range([0, width]);
  g.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).ticks(12).tickFormat(d => monthNames[d - 1]))
    .append("text")
    .attr("x", width / 2)
    .attr("y", 40)
    .attr("fill", "#000")
    .attr("text-anchor", "middle")
    .attr("class", "axis-label")
    .text("Month");

  const minVal = d3.min(grouped, d => Math.min(d.meanVal, d.medianVal));
  const maxVal = d3.max(grouped, d => Math.max(d.meanVal, d.medianVal));
  const y = d3.scaleLinear()
    .domain([minVal, maxVal])
    .nice()
    .range([height, 0]);
  g.append("g")
    .call(d3.axisLeft(y))
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -45)
    .attr("fill", "#000")
    .attr("text-anchor", "middle")
    .attr("class", "axis-label")
    .text(variable.toUpperCase());

  drawLinesAndCircles(g, grouped, x, y, d => d.month, d => d.meanVal, d => d.medianVal, "Month", variable);
}

// correlation heatmap
function drawCorrelationHeatmap(containerSelector, allData, variables) {
  const corrData = [];
  variables.forEach(v1 => {
    variables.forEach(v2 => {
      const arr1 = allData.map(d => d[v1]);
      const arr2 = allData.map(d => d[v2]);
      const corr = pearsonCorrelation(arr1, arr2);
      corrData.push({ var1: v1, var2: v2, correlation: corr });
    });
  });

  const container = d3.select(containerSelector)
    .append("div")
    .attr("class", "chart-container");

  container.append("div")
    .attr("class", "chart-title")
    .text("Correlation Heatmap - All Years Combined");

  const svgWidth = 600, svgHeight = 600;
  const margin = { top: 50, right: 60, bottom: 50, left: 50 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const colorScale = d3.scaleSequential(d3.interpolateRdBu)
    .domain([-1, 1]);

  const gridSize = Math.floor(width / variables.length);

  g.selectAll(".corr-rect")
    .data(corrData)
    .enter().append("rect")
    .attr("class", "corr-rect")
    .attr("x", d => variables.indexOf(d.var1) * gridSize)
    .attr("y", d => variables.indexOf(d.var2) * gridSize)
    .attr("width", gridSize)
    .attr("height", gridSize)
    .attr("fill", d => colorScale(d.correlation))
    .attr("stroke", "#fff")
    .attr("stroke-width", 1)
    .on("mouseover", (event, d) => {
      showTooltip(event, `Vars: ${d.var1} &amp; ${d.var2}<br>Corr: ${d.correlation.toFixed(2)}`);
    })
    .on("mouseout", hideTooltip);

  // correlation text
  g.selectAll(".corr-text")
    .data(corrData)
    .enter().append("text")
    .attr("x", d => variables.indexOf(d.var1) * gridSize + gridSize / 2)
    .attr("y", d => variables.indexOf(d.var2) * gridSize + gridSize / 2)
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .style("font-size", "10px")
    .text(d => d.correlation.toFixed(2));

  // variable labels
  variables.forEach((v, i) => {
    g.append("text")
      .attr("x", i * gridSize + gridSize / 2)
      .attr("y", -5)
      .attr("text-anchor", "middle")
      .attr("class", "axis-label")
      .text(v);
    g.append("text")
      .attr("x", -5)
      .attr("y", i * gridSize + gridSize / 2)
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("class", "axis-label")
      .text(v);
  });

  // Legend
  const legendHeight = 200;
  const legendWidth = 10;
  const legendX = width + 10;
  const legendY = (height - legendHeight) / 2;

  const legendScale = d3.scaleLinear()
    .domain(colorScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale).ticks(5);

  const legendG = g.append("g")
    .attr("transform", `translate(${legendX},${legendY})`);

  const legendData = d3.range(legendHeight);
  legendG.selectAll(".legend-rect")
    .data(legendData)
    .enter().append("rect")
    .attr("class", "legend-rect")
    .attr("x", 0)
    .attr("y", d => d)
    .attr("width", legendWidth)
    .attr("height", 1)
    .attr("fill", d => {
      const t = 1 - d / legendHeight;
      const corrVal = legendScale.invert(t * legendHeight);
      return colorScale(corrVal);
    });

  legendG.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);

  legendG.append("text")
    .attr("x", legendWidth / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text("Correlation");
}

// Daily no of entries (Bar Chart)
function drawDailyBarChart(containerSelector, yearData, variable, year) {
  const filteredYearData = yearData.filter(d => !isNaN(d[variable]));

  // d.date is for daily counts
  const entryCounts = Array.from(
    d3.rollup(filteredYearData, v => v.length, d => d.date),
    ([date, count]) => ({ date: new Date(date), count })
  ).sort((a, b) => d3.ascending(a.date, b.date));

  const container = d3.select(containerSelector)
    .append("div")
    .attr("class", "chart-container");

  container.append("div")
    .attr("class", "chart-title")
    .text(`Daily Entry Counts - ${variable.toUpperCase()} - Year ${year}`);

  const svgWidth = 900, svgHeight = 500;
  const margin = { top: 20, right: 30, bottom: 50, left: 60 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const xDomain = entryCounts.map(d => d3.timeFormat("%Y-%m-%d")(d.date));
  const x = d3.scaleBand()
    .domain(xDomain)
    .range([0, width])
    .padding(0.1);

  // Show fewer x‐axis ticks to avoid cluttering
  const tickValues = xDomain.filter((_, i) => i % 7 === 0);
  const xAxis = d3.axisBottom(x).tickValues(tickValues);

  g.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(xAxis)
    .selectAll("text")
    .attr("transform", "rotate(-45)")
    .style("text-anchor", "end");

  const y = d3.scaleLinear()
    .domain([0, d3.max(entryCounts, d => d.count)])
    .nice()
    .range([height, 0]);
  g.append("g").call(d3.axisLeft(y));

  g.selectAll(".bar")
    .data(entryCounts)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", d => x(d3.timeFormat("%Y-%m-%d")(d.date)))
    .attr("y", d => y(d.count))
    .attr("width", x.bandwidth())
    .attr("height", d => height - y(d.count))
    .attr("fill", "teal")
    .on("mouseover", (event, d) => {
      showTooltip(event, `Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Count: ${d.count}`);
    })
    .on("mouseout", hideTooltip);
}

// calendar heatmap
function drawCalendarHeatmap(containerSelector, yearData, variable, year) {
  const grouped = d3.rollups(
    yearData,
    v => d3.mean(v, d => d[variable]),
    d => d.month,
    d => d.day
  );

  let calData = [];
  grouped.forEach(([m, dayArray]) => {
    dayArray.forEach(([day, val]) => {
      calData.push({ month: m, day: day, value: val });
    });
  });

  const container = d3.select(containerSelector)
    .append("div")
    .attr("class", "chart-container");

  container.append("div")
    .attr("class", "chart-title")
    .text(`${variable.toUpperCase()} Calendar Heatmap - Year ${year}`);

  const svgWidth = 800, svgHeight = 400;
  const margin = { top: 50, right: 70, bottom: 20, left: 60 };
  const width = svgWidth - margin.left - margin.right;
  const height = svgHeight - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  const months = d3.range(1, 13);
  const days = d3.range(1, 32);
  const cellWidth = width / 31;
  const cellHeight = height / 12;

  const calValues = calData.map(d => d.value).filter(v => !isNaN(v));
  const [minVal, maxVal] = d3.extent(calValues);
  const colorScale = d3.scaleSequential(d3.interpolateViridis)
    .domain([minVal, maxVal]);

  const lookup = {};
  calData.forEach(d => {
    lookup[`${d.month}-${d.day}`] = d.value;
  });

  months.forEach((m, rowIndex) => {
    days.forEach(day => {
      const key = `${m}-${day}`;
      const val = lookup[key];
      g.append("rect")
        .attr("x", (day - 1) * cellWidth)
        .attr("y", rowIndex * cellHeight)
        .attr("width", cellWidth)
        .attr("height", cellHeight)
        .attr("fill", val !== undefined ? colorScale(val) : "#eee")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1)
        .on("mouseover", (event) => {
          if (val !== undefined) {
            showTooltip(event, `<strong>${variable.toUpperCase()}</strong><br>Year: ${year}<br>Month-Day: ${m}-${day}<br>Value: ${val.toFixed(2)}`);
          }
        })
        .on("mouseout", hideTooltip);
    });
  });

  // month labels
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  months.forEach((m, i) => {
    g.append("text")
      .attr("x", -10)
      .attr("y", i * cellHeight + cellHeight / 2)
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .style("font-size", "10px")
      .text(monthNames[m - 1]);
  });

  // Legend
  const legendHeight = 150;
  const legendWidth = 10;
  const legendX = width + 10;
  const legendY = (height - legendHeight) / 2;

  const legendScale = d3.scaleLinear()
    .domain(colorScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale).ticks(5);

  const legendG = g.append("g")
    .attr("transform", `translate(${legendX},${legendY})`);

  const legendData = d3.range(legendHeight);
  legendG.selectAll(".legend-rect")
    .data(legendData)
    .enter().append("rect")
    .attr("class", "legend-rect")
    .attr("x", 0)
    .attr("y", d => d)
    .attr("width", legendWidth)
    .attr("height", 1)
    .attr("fill", d => {
      const t = 1 - d / legendHeight;
      const val = legendScale.invert(t * legendHeight);
      return colorScale(val);
    });

  legendG.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);

  legendG.append("text")
    .attr("x", legendWidth / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(variable.toUpperCase());
}

// Main function to load data and also to select which variables
function loadAndRenderAll(sectionId) {
  // Decide data file & variables for each section
  let dataUrl = "";
  let variables = [];
  switch (sectionId) {
    case "room1":
      dataUrl = "json/mane_room_1.json";
      variables = ["co2", "temperature", "humidity", "pressure", "voc"];
      break;
    case "room2":
      dataUrl = "json/mane_room_2.json";
      variables = ["co2", "temperature", "humidity", "pressure", "voc"];
      break;
    case "freezer":
      dataUrl = "json/freezer.json";
      variables = ["temperature"];
      break;
    case "incubator":
      dataUrl = "json/incubator.json";
      variables = ["inc_co2", "inc_temp"];
      break;
    case "planer":
      dataUrl = "json/planer_inc.json";
      variables = ["temp_a", "temp_b"];
      break;
    case "weight_n2":
      dataUrl = "json/weight_n2.json";
      variables = ["n2"];
      break;
    default:
      return;
  }

  // Data parsing ,the given data has two different date formats
  const parseTimeList = [
    d3.timeParse("%Y-%m-%d %H:%M:%S"), 
    d3.timeParse("%d/%m/%y %H:%M")      
  ];

  function parseTimeStamp(str) {
    for (const p of parseTimeList) {
      const d = p(str);
      if (d) return d;
    }
    return null;
  }

  // Load JSON data
  d3.json(dataUrl).then(data => {
    data.forEach(d => {
      const parsedDate = parseTimeStamp(d.time_stamp);
      d.time_stamp = parsedDate;
      variables.forEach(v => {
        d[v] = +d[v];
      });
      d.hour = d.time_stamp.getHours();
      d.weekday = (d.time_stamp.getDay() + 6) % 7;
      d.month = d.time_stamp.getMonth() + 1;
      d.day = d.time_stamp.getDate();
      d.year = d.time_stamp.getFullYear();
      d.date = d3.timeFormat("%Y-%m-%d")(d.time_stamp);
    });
    // Get years and sorting them in ascending order
    const allYears = [...new Set(data.map(d => d.year))].sort(d3.ascending);

    // For each year, draw hourly, weekly, and monthly variation charts for each variable
    allYears.forEach(year => {
      variables.forEach(variable => {
        const yearData = data.filter(r => r.year === year);
        drawHourlyChart(`#${sectionId}`, yearData, variable, year);
        drawWeeklyChart(`#${sectionId}`, yearData, variable, year);
        drawMonthlyChart(`#${sectionId}`, yearData, variable, year);
      });
    });

    // Draw Correlation Heatmap for all data
    drawCorrelationHeatmap(`#${sectionId}`, data, variables);

    // Draw Daily Entry Counts
    variables.forEach(variable => {
      allYears.forEach(year => {
        const yearData = data.filter(r => r.year === year);
        drawDailyBarChart(`#${sectionId}`, yearData, variable, year);
      });
    });

    // Draw Calendar Heatmap
    variables.forEach(variable => {
      allYears.forEach(year => {
        const yearData = data.filter(r => r.year === year);
        drawCalendarHeatmap(`#${sectionId}`, yearData, variable, year);
      });
    });
  });
}
