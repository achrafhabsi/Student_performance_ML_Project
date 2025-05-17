// Get data from the script tag in HTML

// Get data from the hidden div
var chartData = document.getElementById("chart-data");

var studentsAtRisk = parseInt(chartData.getAttribute("data-students-at-risk")) || 0;
var studentsNotAtRisk = parseInt(chartData.getAttribute("data-students-not-at-risk")) || 0;
var teachersAtRisk = parseInt(chartData.getAttribute("data-teachers-at-risk")) || 0;
var teachersNotAtRisk = parseInt(chartData.getAttribute("data-teachers-not-at-risk")) || 0;

console.log(studentsAtRisk, studentsNotAtRisk, teachersAtRisk, teachersNotAtRisk);


// Dynamically load Chart.js
var script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/npm/chart.js";
script.onload = function () {
    console.log("Chart.js loaded successfully!");
    initializeCharts(); // Call function to draw charts after loading
};
document.head.appendChild(script);

// Function to initialize charts after Chart.js loads
function initializeCharts() {
    var ctx1 = document.getElementById('studentsRiskChart');
    if (ctx1) {
        new Chart(ctx1.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['At Risk', 'Not at Risk'],
                datasets: [{
                    label: 'Students Risk Status',
                    data: [studentsAtRisk, studentsNotAtRisk],
                    backgroundColor: ['#FF4C4C', '#32CD32'],
                    borderColor: ['#FF4C4C', '#32CD32'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    var ctx2 = document.getElementById('teachersRiskChart');
    if (ctx2) {
        new Chart(ctx2.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['At Risk', 'Not at Risk'],
                datasets: [{
                    label: 'Teachers Risk Status',
                    data: [teachersAtRisk, teachersNotAtRisk],
                    backgroundColor: ['#FF4C4C', '#32CD32'],
                    borderColor: ['#FF4C4C', '#32CD32'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
}


// Function to toggle visibility of sections
function showDiv(divId) {
    // Hide all divs
    const divs = ['students', 'teachers', 'classes', 'Recomandations'];
    divs.forEach(div => {
        let element = document.getElementById(div);
        if (element) element.style.display = 'none';
    });

    // Show the clicked div
    let selectedDiv = document.getElementById(divId);
    if (selectedDiv) selectedDiv.style.display = 'block';
}



// Function to update email list
function updateEmail(checkbox) {
    var textarea = document.getElementById("message");
    if (!textarea) return;

    console.log("Checkbox checked: " + checkbox.checked);
    console.log("Email value: " + checkbox.value);

    if (checkbox.checked) {
        textarea.value += textarea.value.trim() ? "\n" + checkbox.value : checkbox.value;
    } else {
        textarea.value = textarea.value.split("\n").filter(email => email !== checkbox.value).join("\n");
    }
}
