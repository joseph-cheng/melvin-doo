let _table_ = document.createElement('table'),
    _tr_ = document.createElement('tr'),
    _th_ = document.createElement('th'),
    _td_ = document.createElement('td'),
    _canvas_ = document.createElement('canvas');

function getNames() {
    fetch('http://localhost:5000/members').then((response) => response.json()).then((data) => {
        $(document).ready(function () {
            $('input.autocomplete').autocomplete({
                data: data
            });
        });
    });
}

// TODO: remove get prefix & make consistent with above endpoint
// function getCongresspersonData(congressperson, votesDiv) {
//     c = "Representative Ryan, Paul D."
//     fetch('http://localhost:5000/get_congressperson_bills?name=' + c).then((response) => {
//         return response.json();
//     }).then((response) => {
//         console.log(response);
//         votesDiv.appendChild(buildVotesTable(response['votes']));
//         //tradesDiv.appendChild(buildTradesTable(response['trades']));
//     });
// }

function getStockData(ticker, start, end, chartCanvas) {
    fetch(`http://localhost:5000/stocks?ticker=${ticker}&start=${start}&end=${end}`).then((response) => {
        return response.json();
    }).then((response) => {
        console.log(response);
        buildChart(response['data'], start, end, chartCanvas);
    });
}

function buildChart(data, start, end, chartCanvas) {
    const ctx = chartCanvas.getContext('2d');
    const newdata = linSpaceZip(start, end, data.length, data);
    const labels = linSpace(0, data.length, newdata.length, data);

    const chartData = {
        labels: labels,
        datasets: [{
            label: "Price",
            data: newdata,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.0,
        }]
    };

    const annotation = {
        type: "line",
        mode: "vertical",
        scaleID: "x",
        value: 30,
        borderColor: "red",
        borderWidth: 1,
    };

    const chart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            plugins: {
                annotation: {
                    annotations: {
                        annotation
                    }
                }
            }
        }
    });
}


// Builds the HTML Table out of myList json data from Ivy restful service.
function buildVotesTable(arr) {
    let table = _table_.cloneNode(false),
        columns = addAllColumnHeaders(arr, table);
    for (let i = 0, maxi = 3; i < maxi; ++i) {
        let tr = _tr_.cloneNode(false);
        // let a = document.createElement("a");
        arr[i]['Bill'] = arr[i]['Bill'][0].toUpperCase() + arr[i]['Bill'].substring(1)
        arr[i]['Bill'] += '.';
        tr.addEventListener("click", () => { showTrades(67, arr[i]['Name']) })
        tr.classList.add("vote-row")
        // tr.appendChild(a);
        for (let j = 0, maxj = columns.length; j < maxj; ++j) {
            let td = _td_.cloneNode(false);
            cellValue = arr[i][columns[j]];
            td.appendChild(document.createTextNode(arr[i][columns[j]] || ''));
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    return table;
}

function buildTradesTable(arr) {
    let table = _table_.cloneNode(false),
        columns = addAllColumnHeaders(arr, table);

    let start = new Date('January 23, 2020');
    let end = new Date('January 23, 2022');
    let chartCanvas = document.getElementById("chartCanvas");
    getStockData('GOOG', start.toJSON(), end.toJSON(), chartCanvas);
    for (let i = 0; i < arr.length; ++i) {
        let tr = _tr_.cloneNode(false);
        tr.addEventListener('click', () => { getStockData(arr[i]['ticker'], start, end, chartCanvas)})
        for (let j = 0, maxj = columns.length; j < maxj; ++j) {
            let td = _td_.cloneNode(false);
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
    let columnSet = [],
        tr = _tr_.cloneNode(false);
    for (let i = 0, l = arr.length; i < l; i++) {
        for (let key in arr[i]) {
            if (arr[i].hasOwnProperty(key) && columnSet.indexOf(key) === -1) {
                columnSet.push(key);
                let th = _th_.cloneNode(false);
                th.appendChild(document.createTextNode(key));
                tr.appendChild(th);
            }
        }
    }
    table.appendChild(tr);
    return columnSet;
}

function linSpace(start, end, cardinality, data) {
    let arr = [];
    for (let i = 0; i < cardinality; i++) {
        let date = data[i][0];
        date = date.split(', ')[1].split(' ').slice(0, 3).join(' ');
        arr.push(date);
    }
    return arr;
}

function linSpaceZip(start, end, cardinality, data) {
    let arr = [];
    for (let i = 0; i < cardinality; i++) {
        let date = data[i][0];
        date = date.split(', ')[1].split(' ').slice(0, 3).join(' ');
        arr.push({x: date, y: data[i][1]});
    }
    return arr;
}

let showTrades = (billID, name) => {
    var tradesDiv = document.getElementById("tradesTable");
    tradesDiv.innerHTML = '';
    fetch(`http://localhost:5000/trades?billID=${billID}&name=${name}`).then((response) => {
        return response.json();
    }).then((response) => {
        console.log(response);
        tradesDiv.appendChild(buildTradesTable(response['trades']));
    });
}

let showVotes = (name) => {
    var votesDiv = document.getElementById("tradesTable");
    votesDiv.innerHTML = '';
    fetch(`http://localhost:5000/get_congressperson_bills?name=${name}`).then((response) => {
        return response.json();
    }).then((response) => {
        console.log(response);
        votesDiv.appendChild(buildVotesTable(response['votes']));
    });
}


let displayTable = () => {
    let input = document.getElementById("autocomplete-input")
    input.addEventListener("keyup", (e) => {
        if (e.keyCode == 13) {
            showVotes(input.value)
        }
    })
    // let votesDiv = document.getElementById("votesTable");
    // var tradesDiv = document.getElementById("tradesTable");
    // getCongresspersonData("Representative Cole, Tom", votesDiv);
}
