function validateDOB(selectedDate) {
    var today = new Date();
    var inputDate = new Date(selectedDate);

    // Check if the selected date is in the future
    if (inputDate > today) {
        document.getElementById("dob-error").style.display = "block";
        document.getElementById("birthdate").value = ""; // Clear the input
    } else {
        document.getElementById("dob-error").style.display = "none";
    }
    }