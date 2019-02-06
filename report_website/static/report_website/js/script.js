window.onload = function () {
    let ctx = document.getElementById("chart").getContext("2d");
    gradientFill = ctx.createLinearGradient(0, 0, 0, 150);
    gradientFill.addColorStop(0, "#15D1FA");
    gradientFill.addColorStop(1, "rgba(21, 209, 250, 0)");
    let MONTHS = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ];
    let config = {
        type: "line",
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
                {
                    label: "PM 2.5",
                    backgroundColor: window.gradientFill,
                    borderColor: "#0FAACC",
                    data: [40, 50, 120, 300, 150, 90, 50],
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: false
            },
            tooltips: {
                mode: "index",
                intersect: false
            },
            hover: {
                mode: "nearest",
                intersect: true
            },
            scales: {
                xAxes: [
                    {
                        display: false,
                        scaleLabel: {
                            display: true,
                            labelString: "Month"
                        }
                    }
                ],
                yAxes: [
                    {
                        display: false,
                        scaleLabel: {
                            display: true,
                            labelString: "Value"
                        }
                    }
                ]
            },
            legend: { display: false },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 4,
                    bottom: 0
                }
            }
        }
    };

    window.chart = new Chart(ctx, config);
};

const openModal = function (modalId) {
    document.getElementById(modalId).classList.remove('closed');
}
const closeModal = function (modalId) {
    document.getElementById(modalId).classList.add('closed');
}
