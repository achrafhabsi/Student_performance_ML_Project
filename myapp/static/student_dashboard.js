// Get data from hidden div
var chartData = document.getElementById("chart-data");

var studentAbsences = parseInt(chartData.getAttribute("data-student-absences")) || 0;
var meanAbsences = parseInt(chartData.getAttribute("data-mean-absences")) || 0;
var studentG3 = parseInt(chartData.getAttribute("data-student-g3")) || 0;
var meanG3 = parseInt(chartData.getAttribute("data-mean-g3")) || 0;
var studentStudyTime = parseInt(chartData.getAttribute("data-student-studytime")) || 0;
var meanStudyTime = parseInt(chartData.getAttribute("data-mean-studytime")) || 0;

// Absence Chart
const absenceCtx = document.getElementById('absenceChart').getContext('2d');
new Chart(absenceCtx, {
    type: 'bar',
    data: {
        labels: ['Current Student', 'Class Mean'],
        datasets: [{
            label: 'Absences',
            data: [studentAbsences, meanAbsences],
            backgroundColor: 'rgba(255, 99, 132, 0.5)'
        }]
    }
});

// G3 Score Chart
const G3Ctx = document.getElementById('G3Chart').getContext('2d');
new Chart(G3Ctx, {
    type: 'bar',
    data: {
        labels: ['Current Student', 'Class Mean'],
        datasets: [{
            label: 'G3 Score',
            data: [studentG3, meanG3],
            borderColor: 'rgba(54, 162, 235, 1)',
            fill: false
        }]
    }
});

// Study Time Chart
const studyTimeCtx = document.getElementById('studyTimeChart').getContext('2d');
new Chart(studyTimeCtx, {
    type: 'bar',
    data: {
        labels: ['Current Student', 'Class Mean'],
        datasets: [{
            label: 'Study Time',
            data: [studentStudyTime, meanStudyTime],
            backgroundColor: ['#FF6384', '#36A2EB']
        }]
    }
});
