let _table_ = document.createElement('table'),
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

function getStockData(ticker, start, end, chartCanvas) ***REMOVED***
    fetch(`http://localhost:5000/stocks?ticker=$***REMOVED***ticker***REMOVED***&start=$***REMOVED***start***REMOVED***&end=$***REMOVED***end***REMOVED***`).then((response) => ***REMOVED***
        return response.json();
    ***REMOVED***).then((response) => ***REMOVED***
        console.log(response);
        buildChart(response['data'], start, end, chartCanvas);
    ***REMOVED***);
***REMOVED***

function buildChart(data, start, end, chartCanvas) ***REMOVED***
    const ctx = chartCanvas.getContext('2d');
    const newdata = linSpaceZip(start, end, data.length, data);
    const labels = linSpace(0, data.length, newdata.length, data);

    const chartData = ***REMOVED***
        labels: labels,
        datasets: [***REMOVED***
            label: "Price",
            data: newdata,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.0,
        ***REMOVED***]
    ***REMOVED***;

    const annotation = ***REMOVED***
        type: "line",
        mode: "vertical",
        scaleID: "x",
        value: 30,
        borderColor: "red",
        borderWidth: 1,
    ***REMOVED***;

    const chart = new Chart(ctx, ***REMOVED***
        type: 'line',
        data: chartData,
        options: ***REMOVED***
            plugins: ***REMOVED***
                annotation: ***REMOVED***
                    annotations: ***REMOVED***
                        annotation
                    ***REMOVED***
                ***REMOVED***
            ***REMOVED***
        ***REMOVED***
    ***REMOVED***);
***REMOVED***


// Builds the HTML Table out of myList json data from Ivy restful service.
function buildHtmlTable(arr) ***REMOVED***
    let table = _table_.cloneNode(false),
        columns = addAllColumnHeaders(arr, table);
    for (let i = 0, maxi = arr.length; i < maxi; ++i) ***REMOVED***
        let tr = _tr_.cloneNode(false);
        for (let j = 0, maxj = columns.length; j < maxj; ++j) ***REMOVED***
            let td = _td_.cloneNode(false);
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
    let columnSet = [],
        tr = _tr_.cloneNode(false);
    for (let i = 0, l = arr.length; i < l; i++) ***REMOVED***
        for (let key in arr[i]) ***REMOVED***
            if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1) ***REMOVED***
                columnSet.push(key);
                let th = _th_.cloneNode(false);
                th.appendChild(document.createTextNode(key));
                tr.appendChild(th);
            ***REMOVED***
        ***REMOVED***
    ***REMOVED***
    table.appendChild(tr);
    return columnSet;
***REMOVED***

function linSpace(start, end, cardinality, data) ***REMOVED***
    let arr = [];
    for (let i = 0; i < cardinality; i++) ***REMOVED***
        let date = data[i][0];
        date = date.split(', ')[1].split(' ').slice(0, 3).join(' ');
        arr.push(date);
    ***REMOVED***
    return arr;
***REMOVED***

function linSpaceZip(start, end, cardinality, data) ***REMOVED***
    let arr = [];
    for (let i = 0; i < cardinality; i++) ***REMOVED***
        let date = data[i][0];
        date = date.split(', ')[1].split(' ').slice(0, 3).join(' ');
        arr.push(***REMOVED***x: date, y: data[i][1]***REMOVED***);
    ***REMOVED***
    return arr;
***REMOVED***


let displayTable = () => ***REMOVED***
    let votesDiv = document.getElementById("votesTable");
    let tradesDiv = document.getElementById("tradesTable");
    let chartCanvas = document.getElementById("chartCanvas");
    getCongresspersonData("testdata", votesDiv, tradesDiv);

    let start = new Date('August 19, 2019');
    let end = new Date('March 9, 2020');
    getStockData('GOOG', start.toJSON(), end.toJSON(), chartCanvas);
***REMOVED***
