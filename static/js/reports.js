var socket = io()

async function generateWinsReport() {
    socket.emit('generate-wins-report', {});
    let reportData;
    function handleResponse(data) {
        reportData = data;
    }
    socket.on('receive-wins-report', handleResponse);
    while (reportData == undefined) {
        await new Promise(r => setTimeout(r, 100))  // Waits for 100 ms.
    }
    let percentages = reportData.win_percentages;
    let winsReportData = [{
        type: 'bar',
        x: ['Croupier', 'Ai1', 'Ai2', 'Human'],
        y: percentages,
        width: [0.5, 0.5, 0.5, 0.5],
        automargin: true
    }];
    let winsReportLayout = {
        height: 300,
        width: 550,
        margin: { 't': 30, 'b': 30, 'l': 30, 'r': 30 },
        showlegend: false,
        paper_bgcolor: "rgba(0, 0, 0, 0)",
        plot_bgcolor: "rgba(128, 128, 128, 0.2)",
        barcornerradius: 5,
        font: {
            color: "#fff"
        }
    };
    Plotly.newPlot('wins-report', winsReportData, winsReportLayout);
}

async function generateDecisionsReport() {
    socket.emit('generate-decisions-report', {});
    let reportData;
    function handleResponse(data) {
        reportData = data;
    }
    socket.on('receive-decisions-report', handleResponse);
    while (reportData == undefined) {
        await new Promise(r => setTimeout(r, 100))  // Waits for 100 ms.
    }
    let percentages = reportData.success_percentages;

    let decisionsReportData = [{
        type: 'bar',
        x: ['Croupier', 'Ai1', 'Ai2', 'Human'],
        y: percentages,
        width: [0.5, 0.5, 0.5, 0.5],
        automargin: true
    }];
    let decisionsReportLayout = {
        height: 300,
        width: 550,
        margin: { 't': 30, 'b': 30, 'l': 30, 'r': 30 },
        showlegend: false,
        paper_bgcolor: "rgba(0, 0, 0, 0)",
        plot_bgcolor: "rgba(128, 128, 128, 0.2)",
        barcornerradius: 5,
        font: {
            color: "#fff"
        }
    };
    Plotly.newPlot('decisions-report', decisionsReportData, decisionsReportLayout);
}

async function generateStandReport() {
    socket.emit('generate-stand-report', {});
    let reportData;
    function handleResponse(data) {
        reportData = data;
    }
    socket.on('receive-stand-report', handleResponse);
    while (reportData == undefined) {
        await new Promise(r => setTimeout(r, 100))  // Waits for 100 ms.
    }

    let croupierStandValues = reportData.croupier;
    let ai1StandValues = reportData.ai1;
    let ai2StandValues = reportData.ai2;
    let humanStandValues = reportData.human;
    let gamesIndices = Array.from({length:croupierStandValues.length}, (v,k)=>k+1);

    if (gamesIndices.length == 0) {
        return;
    }

    let croupierTrace = {
        x: gamesIndices,
        y: croupierStandValues,
        type: 'scatter',
        name: 'Croupier'
    };

    let ai1Trace = {
        x: gamesIndices,
        y: ai1StandValues,
        type: 'scatter',
        name: 'Ai 1'
    };

    let ai2Trace = {
        x: gamesIndices,
        y: ai2StandValues,
        type: 'scatter',
        name: 'Ai 2'
    };

    let humanTrace = {
        x: gamesIndices,
        y: humanStandValues,
        type: 'scatter',
        name: 'Player'
    };

    let standReportData = [croupierTrace, ai1Trace, ai2Trace, humanTrace];

    let standReportLayout = {
        height: 300,
        width: 550,
        paper_bgcolor: "rgba(0, 0, 0, 0)",
        plot_bgcolor: "rgba(128, 128, 128, 0.2)",
        margin: { 't': 30, 'b': 30, 'l': 30, 'r': 30 },
        font: {
            color: "#fff"
        }
    };
    Plotly.newPlot('stand-report', standReportData, standReportLayout);
}


function toggleReports() {
    let reportsWindow = document.getElementById('reports-window');
    if (reportsWindow.style.display === '') {
        reportsWindow.style.display = 'flex';
    } else {
        reportsWindow.style.display = '';
    }
    showWinsReport();
}
window.toggleReports = toggleReports;

function hideDiv(id) {
    document.getElementById(id).style.display = '';
}

function showDiv(id) {
    document.getElementById(id).style.display = 'flex';
}

function showWinsReport() {
    generateWinsReport();
    showDiv('wins-report');
    hideDiv('decisions-report');
    hideDiv('stand-report');
}
window.showWinsReport = showWinsReport;

function showDecisionsReport() {
    generateDecisionsReport();
    showDiv('decisions-report');
    hideDiv('wins-report');
    hideDiv('stand-report');
}

window.showDecisionsReport = showDecisionsReport;

function showStandReport() {
    generateStandReport();
    showDiv('stand-report');
    hideDiv('decisions-report');
    hideDiv('wins-report');
}
window.showStandReport = showStandReport;