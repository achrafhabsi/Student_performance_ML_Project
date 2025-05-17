document.addEventListener("DOMContentLoaded", function() {
    // Get data from hidden div
    var chartData = document.getElementById("chart-data");

    var studentsZero = parseInt(chartData.getAttribute("data-students-zero")) || 0;
    var studentsOne = parseInt(chartData.getAttribute("data-students-one")) || 0;
    var studentsOther = parseInt(chartData.getAttribute("data-students-other")) || 0;

    var ctx = document.getElementById('studentResultsChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Students with Result 0', 'Students with Result 1', 'Other Results'],
            datasets: [{
                data: [studentsZero, studentsOne, studentsOther],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
});
