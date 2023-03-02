const alertBox = document.getElementById("alertbox");
const closeBtn = alertBox.querySelector(".closebtn");

if (sessionStorage.getItem("alertShown") === "false") {
    alertBox.style.display = "block"; // Show the box
}

closeBtn.addEventListener("click", function () {
    sessionStorage.setItem("alertShown", "true");
    alertBox.style.display = "none"; // Hide the box when close button is clicked
});
