// eslint-disable-next-line no-unused-vars
function show_toast(message) {
    const toast_message = document.querySelector("#toast-message");
    toast_message.textContent = message;
    const toast_container = document.querySelector("#toast-container");
    toast_container.style.display = "block";
}

// eslint-disable-next-line no-unused-vars
function hide_toast() {
    const toast_container = document.querySelector("#toast-container");
    toast_container.style.display = "none";
}

// eslint-disable-next-line no-unused-vars
function hide_toast_success_msg() {
    const toast_msg = $(".toast-success-message")[0];
    toast_msg.style.display = "none";
}

function is_valid_email(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function is_valid_url(url) {
    const urlPattern = /^(https?:\/\/)?[a-z0-9-]+\.[a-z]{2,}(\.[a-z]{2,})?$/i;
    return urlPattern.test(url);
}

function is_valid_tel_number(input_str) {
    var re = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/;

    return re.test(input_str);
}

// eslint-disable-next-line no-unused-vars,complexity
function form_submit_action() {
    // URL Change
    var test = $(".s_website_form");
    var form = test.find("form");

    var program_id = $("#program_submit_id");

    form[0].action = `/selfservice/submitted/${program_id[0].getAttribute("program")}`;

    // Validation's //
    var isValid = true;

    var required_fields = $(".s_website_form_required");

    for (let i = 0; i < required_fields.length; i++) {
        var required_input_field = required_fields[i].getElementsByClassName("s_website_form_input")[0];
        var field_name = required_input_field.name.toLowerCase();
        var error_message = '<div class="input-field-error-message">Please enter ' + field_name + "</div>";

        // Null value
        if (required_input_field.value === "") {
            required_input_field.style.borderColor = "#D32D2D";
            isValid = false;
            show_toast("Please update all mandatory fields");

            if (required_input_field.type === "radio" || required_input_field.type === "checkbox") {
                // Pass
            } else if (required_fields[i].getElementsByClassName("input-field-error-message").length === 0) {
                required_fields[i].insertAdjacentHTML("beforeend", error_message);
            } else {
                if (
                    required_fields[i].getElementsByClassName("input-field-validation-message").length !== 0
                ) {
                    required_fields[i].getElementsByClassName(
                        "input-field-validation-message"
                    )[0].style.display = "none";
                }
                required_fields[i].getElementsByClassName("input-field-error-message")[0].style.display =
                    "block";
            }
        }

        // Checking valid value
        else {
            required_input_field.style.borderColor = "#E3E3E3";
            // Removing the error message of not filling the input field
            if (required_fields[i].getElementsByClassName("input-field-error-message").length !== 0) {
                required_fields[i].getElementsByClassName("input-field-error-message")[0].style.display =
                    "none";
            }

            if (required_fields[i].getElementsByClassName("input-field-validation-message").length !== 0) {
                required_fields[i].getElementsByClassName("input-field-validation-message")[0].style.display =
                    "none";
            }

            if (required_input_field.type === "email") {
                if (is_valid_email(required_input_field.value) === false) {
                    isValid = false;
                    const validation_message =
                        '<div class="input-field-validation-message">Please enter a valid email address</div>';
                    required_input_field.style.borderColor = "#D32D2D";
                    show_toast("Please update all mandatory fields");

                    if (
                        required_fields[i].getElementsByClassName("input-field-validation-message").length ===
                        0
                    ) {
                        required_fields[i].insertAdjacentHTML("beforeend", validation_message);
                    } else {
                        required_fields[i].getElementsByClassName(
                            "input-field-validation-message"
                        )[0].style.display = "block";
                    }
                }
            } else if (required_input_field.type === "url") {
                if (is_valid_url(required_input_field.value) === false) {
                    isValid = false;
                    const validation_message =
                        '<div class="input-field-validation-message">Please enter a valid url</div>';
                    show_toast("Please update all mandatory fields");
                    required_input_field.style.borderColor = "#D32D2D";

                    if (
                        required_fields[i].getElementsByClassName("input-field-validation-message").length ===
                        0
                    ) {
                        required_fields[i].insertAdjacentHTML("beforeend", validation_message);
                    } else {
                        required_fields[i].getElementsByClassName(
                            "input-field-validation-message"
                        )[0].style.display = "block";
                    }
                }
            } else if (required_input_field.type === "tel") {
                if (is_valid_tel_number(required_input_field.value) === false) {
                    isValid = false;
                    const validation_message =
                        '<div class="input-field-validation-message">Please enter a valid telephone number</div>';
                    show_toast("Please update all mandatory fields");
                    required_input_field.style.borderColor = "#D32D2D";

                    if (
                        required_fields[i].getElementsByClassName("input-field-validation-message").length ===
                        0
                    ) {
                        required_fields[i].insertAdjacentHTML("beforeend", validation_message);
                    } else {
                        required_fields[i].getElementsByClassName(
                            "input-field-validation-message"
                        )[0].style.display = "block";
                    }
                }
            } else if (required_input_field.type === "radio" || required_input_field.type === "checkbox") {
                var options = required_fields[i].getElementsByClassName("form-check-input");
                var isChecked = false;

                for (let j = 0; j < options.length; j++) {
                    // Options[j].style.outline = 'none'

                    if (options[j].checked) {
                        isChecked = true;
                    }
                }

                if (isChecked === false) {
                    isValid = false;
                    var field_name_checked = required_input_field.name.toLowerCase();
                    var select_error_message =
                        '<div class="input-field-error-message">Please select ' +
                        field_name_checked +
                        "</div>";

                    if (required_fields[i].getElementsByClassName("input-field-error-message").length === 0) {
                        required_fields[i].insertAdjacentHTML("beforeend", select_error_message);
                    } else {
                        required_fields[i].getElementsByClassName(
                            "input-field-error-message"
                        )[0].style.display = "block";
                    }

                    // For(let j=0; j<options.length; j++){
                    //   options[j].style.outline = '1px solid #D32D2D'
                    // }
                }
            }
        }
    }

    if (isValid) {
        form.submit();
    }
}

// eslint-disable-next-line no-unused-vars
function toggle_chat_bot() {
    var box = document.getElementById("chat-bot");
    if (box.style.display === "none") {
        box.style.display = "block";
    } else {
        box.style.display = "none";
    }
}
