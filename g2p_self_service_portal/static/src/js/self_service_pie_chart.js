document.addEventListener("DOMContentLoaded", function () {
    var mydata = JSON.parse(document.getElementById("pie_data").textContent);
    console.log(mydata);
    if (mydata.values[0] > 0) {
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
                    align: "center",
                },
                animation: {
                    animateScale: true,
                    animateRotate: true,
                },
            },
        });
    } else {
        const newElement = document.createElement("p");
        newElement.textContent = "In order to see the entitlements, please enroll into a program.";
        newElement.classList.add("no-payments-text");
        document.getElementById("chartContainer").innerHTML = "&nbsp;";
        document.getElementById("chartContainer").appendChild(newElement);
    }
});
