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

function showWinsReport() {
    generateWinsReport();
    let winsReport = document.getElementById('wins-report');
    winsReport.style.display = 'flex'
    let decisionsReport = document.getElementById('decisions-report');
    decisionsReport.style.display = ''
}
window.showWinsReport = showWinsReport;

function showDecisionsReport() {
    generateDecisionsReport();
    let decisionsReport = document.getElementById('decisions-report');
    decisionsReport.style.display = 'flex'
    let winsReport = document.getElementById('wins-report');
    winsReport.style.display = ''
}
window.showDecisionsReport = showDecisionsReport;