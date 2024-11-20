function toggleReports() {
  let reportsWindow = document.getElementById('reports-window');
  if (reportsWindow.hidden) {
    reportsWindow.hidden = false
  } else {
    reportsWindow.hidden = true
  }
}
window.toggleReports = toggleReports;