document.addEventListener('DOMContentLoaded', function() {
    const yearDropdown = document.getElementById('yearDropdown');
    const monthDropdown = document.getElementById('monthDropdown');
    const chartApiUrl = 'http://127.0.0.1:5000/getDailySales';

    let barChart;

    // Get the current year and month
    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1; // Months are 0-indexed

    // Populate the year dropdown with a range of years
    for (let year = currentYear - 10; year <= currentYear + 10; year++) {
        let option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        if (year === currentYear) {
            option.selected = true;
        }
        yearDropdown.appendChild(option);
    }

    // Set the current month as selected
    monthDropdown.value = currentMonth;

    function fetchDataAndUpdateChart() {
        const year = yearDropdown.value;
        const month = monthDropdown.value;

        console.log("Selected Year:", year);
        console.log("Selected Month:", month);

        const requestPayload = {
            year: year,
            month: month
        };

        callApi("POST", chartApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
    }

    function callApi(method, url, data) {
        $.ajax({
            method: method,
            url: url,
            data: data
        }).done(function(response) {
            console.log(response);
            if (response.length > 0) {
                renderChart(response);
                document.getElementById('Nodatafound').style.display = 'none';
                document.getElementById('barChart').style.display = 'block';
            } else {
                document.getElementById('Nodatafound').style.display = 'block';
                document.getElementById('barChart').style.display = 'none';
                document.getElementById('Nodatafound').innerHTML = 'No data found';
            }
        });
    }

    function renderChart(data) {
        // Extracting the year and month from the first date entry
        const firstDate = new Date(data[0]['purchase_date']);
        const year = firstDate.getFullYear();
        const month = firstDate.getMonth();

        // Get the number of days in the selected month
        const numberOfDays = new Date(year, month + 1, 0).getDate();

        // Initialize arrays for labels and totals
        const labels = Array.from({ length: numberOfDays }, (_, i) => i + 1);
        const totals = Array(numberOfDays).fill(0);

        // Update totals for dates with data
        for (let i = 0; i < data.length; i++) {
            const date = new Date(data[i]['purchase_date']);
            const dayOfMonth = date.getDate();
            totals[dayOfMonth - 1] += data[i]['total'];
        }

        // Create the chart
        const ctx = document.getElementById('barChart').getContext('2d');
        if (window.myChart) {
            // If chart already exists, destroy it before creating a new one
            window.myChart.destroy();
        }
        window.myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Sales',
                    data: totals,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Total Value'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }

    yearDropdown.addEventListener('change', fetchDataAndUpdateChart);
    monthDropdown.addEventListener('change', fetchDataAndUpdateChart);

    // Initial fetch to populate the chart
    fetchDataAndUpdateChart();
});
