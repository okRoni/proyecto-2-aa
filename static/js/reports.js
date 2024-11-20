function generateWinsReport() {
    let winsReportData = [{
        type: 'pie',
        values: [1, 3, 7, 2],
        labels: ['Croupier', 'Ai1', 'Ai2', 'Human'],
        textinfo: 'label+percent',
        textposition: 'outside',
        automargin: true
    }];
    let winsReportLayout = {
        height: 300,
        width: 750,
        margin: { 't': 10, 'b': 10, 'l': 10, 'r': 10 },
        showlegend: false,
        paper_bgcolor: "rgba(0, 0, 0, 0)",
        font: {
            color: "#fff"
        }
    };
    Plotly.newPlot('wins-report', winsReportData, winsReportLayout);
}

function generateDecisionsReport() {
    let decisionsReportData = [{
        type: 'pie',
        values: [3, 4, 2, 6],
        labels: ['Croupier', 'Ai1', 'Ai2', 'Human'],
        textinfo: 'label+percent',
        textposition: 'outside',
        automargin: true
    }];
    let decisionsReportLayout = {
        height: 300,
        width: 750,
        margin: { 't': 10, 'b': 10, 'l': 10, 'r': 10 },
        showlegend: false,
        paper_bgcolor: "rgba(0, 0, 0, 0)",
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