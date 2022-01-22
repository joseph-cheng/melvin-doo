var _table_ = document.createElement('table'),
  _tr_ = document.createElement('tr'),
  _th_ = document.createElement('th'),
  _td_ = document.createElement('td'),
  _canvas_ = document.createElement('canvas');

function getCongresspersonData(congressperson, votesDiv, tradesDiv) {
    fetch('http://localhost:5000/get_congressperson_data?name=' + congressperson).then((response) => {
            return response.json();
        }).then((response) => {
            console.log(response);
            votesDiv.appendChild(buildHtmlTable(response['votes']));
            tradesDiv.appendChild(buildHtmlTable(response['trades']));
        });
}

function getStockData(ticker, start, end, chartDiv) {
    fetch('http://localhost:5000/get_stock_data?ticker=' + ticker + '?start=' + start + '?end=' + end).then((response) => {
        return response.json();
    }).then((response) => {
        console.log(response);
        buildChart(response['data'], start, end, chartCanvas);
    });
}

function buildChart(data, start, end, chartCanvas) {
    const ctx = chartCanvas.getContext('2d');

    const chartData = {
        labels: makeArr(start, end, data.length),
        datasets: [{
            label: "Price",
            data: data,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
        }]
    };

    const chart = new Chart(ctx, {
        type: 'line',
        data: chartData
    });


}



// Builds the HTML Table out of myList json data from Ivy restful service.
function buildHtmlTable(arr) {
  var table = _table_.cloneNode(false),
    columns = addAllColumnHeaders(arr, table);
  for (var i = 0, maxi = arr.length; i < maxi; ++i) {
    var tr = _tr_.cloneNode(false);
    for (var j = 0, maxj = columns.length; j < maxj; ++j) {
      var td = _td_.cloneNode(false);
      cellValue = arr[i][columns[j]];
      td.appendChild(document.createTextNode(arr[i][columns[j]] || ''));
      tr.appendChild(td);
    }
    table.appendChild(tr);
  }
  return table;
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(arr, table) {
  var columnSet = [],
    tr = _tr_.cloneNode(false);
  for (var i = 0, l = arr.length; i < l; i++) {
    for (var key in arr[i]) {
      if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1) {
        columnSet.push(key);
        var th = _th_.cloneNode(false);
        th.appendChild(document.createTextNode(key));
        tr.appendChild(th);
      }
    }
  }
  table.appendChild(tr);
  return columnSet;
}

function makeArr(startValue, stopValue, cardinality) {
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
    arr.push(startValue + (step * i));
  }
  return arr;
}

