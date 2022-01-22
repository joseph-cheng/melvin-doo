var _table_ = document.createElement('table'),
  _tr_ = document.createElement('tr'),
  _th_ = document.createElement('th'),
  _td_ = document.createElement('td'),
  _canvas_ = document.createElement('canvas');

function getCongresspersonData(congressperson, votesDiv, tradesDiv) ***REMOVED***
    fetch('http://localhost:5000/get_congressperson_data?name=' + congressperson).then((response) => ***REMOVED***
            return response.json();
        ***REMOVED***).then((response) => ***REMOVED***
            console.log(response);
            votesDiv.appendChild(buildHtmlTable(response['votes']));
            tradesDiv.appendChild(buildHtmlTable(response['trades']));
        ***REMOVED***);
***REMOVED***

function getStockData(ticker, start, end, chartDiv) ***REMOVED***
    fetch('http://localhost:5000/get_stock_data?ticker=' + ticker + '?start=' + start + '?end=' + end).then((response) => ***REMOVED***
        return response.json();
    ***REMOVED***).then((response) => ***REMOVED***
        console.log(response);
        buildChart(response['data'], start, end, chartCanvas);
    ***REMOVED***);
***REMOVED***

function buildChart(data, start, end, chartCanvas) ***REMOVED***
    const ctx = chartCanvas.getContext('2d');

    const chartData = ***REMOVED***
        labels: makeArr(start, end, data.length),
        datasets: [***REMOVED***
            label: "Price",
            data: data,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
        ***REMOVED***]
    ***REMOVED***;

    const chart = new Chart(ctx, ***REMOVED***
        type: 'line',
        data: chartData
    ***REMOVED***);


***REMOVED***



// Builds the HTML Table out of myList json data from Ivy restful service.
function buildHtmlTable(arr) ***REMOVED***
  var table = _table_.cloneNode(false),
    columns = addAllColumnHeaders(arr, table);
  for (var i = 0, maxi = arr.length; i < maxi; ++i) ***REMOVED***
    var tr = _tr_.cloneNode(false);
    for (var j = 0, maxj = columns.length; j < maxj; ++j) ***REMOVED***
      var td = _td_.cloneNode(false);
      cellValue = arr[i][columns[j]];
      td.appendChild(document.createTextNode(arr[i][columns[j]] || ''));
      tr.appendChild(td);
    ***REMOVED***
    table.appendChild(tr);
  ***REMOVED***
  return table;
***REMOVED***

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(arr, table) ***REMOVED***
  var columnSet = [],
    tr = _tr_.cloneNode(false);
  for (var i = 0, l = arr.length; i < l; i++) ***REMOVED***
    for (var key in arr[i]) ***REMOVED***
      if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1) ***REMOVED***
        columnSet.push(key);
        var th = _th_.cloneNode(false);
        th.appendChild(document.createTextNode(key));
        tr.appendChild(th);
      ***REMOVED***
    ***REMOVED***
  ***REMOVED***
  table.appendChild(tr);
  return columnSet;
***REMOVED***

function makeArr(startValue, stopValue, cardinality) ***REMOVED***
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) ***REMOVED***
    arr.push(startValue + (step * i));
  ***REMOVED***
  return arr;
***REMOVED***

