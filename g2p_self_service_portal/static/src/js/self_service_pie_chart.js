document.addEventListener("DOMContentLoaded", function () {
    var mydata = JSON.parse(document.getElementById("pie_data").textContent);
    console.log(mydata);
    document.getElementById("chartContainer").innerHTML = "&nbsp;";
    document.getElementById("chartContainer").innerHTML =
        '<canvas id="myChart" width="150" height="150"></canvas>';
    var ctx = document.getElementById("myChart").getContext("2d");
    // eslint-disable-next-line no-unused-vars,no-undef
    var myChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: mydata.labels,
            datasets: [
                {
                    data: mydata.values,
                    backgroundColor: ["#76D0D9", "#186ADE"],
                    borderColor: ["#76D0D9", "#186ADE"],
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            legend: {
                display: true,
                position: "bottom",
            },
            animation: {
                animateScale: true,
                animateRotate: true,
            },
        },
    });
});
