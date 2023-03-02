const alertBox = document.getElementById("alertbox");
const closeBtn = alertBox.querySelector(".closebtn");

if (sessionStorage.getItem("alertShown") === "false") {
    // Show the box
    alertBox.style.display = "block";
}

closeBtn.addEventListener("click", function () {
    sessionStorage.setItem("alertShown", "true");
    // Hide the box when close button is clicked
    alertBox.style.display = "none";
});
