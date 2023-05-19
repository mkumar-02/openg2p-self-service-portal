// TODO: The following function is part if selfservice portal module too,
// reuse from there.
// eslint-disable-next-line no-unused-vars,complexity
function reimbursement_form_submit_action() {
    // URL Change
    // var test = $(".s_website_form");
    var form = $("#reimbursement-form");

    var program_id = $("#program_submit_id");
    form[0].action = `/serviceprovider/claim/${program_id[0].getAttribute("program")}`;

    console.log(form[0].action);

    // Validation's //
    var isValid = true;

    // Var required_fields = $(".s_website_form_required");

    // for (let i = 0; i < required_fields.length; i++) {
    //     var required_input_field = required_fields[i].getElementsByClassName("s_website_form_input")[0];
    //     var field_name = required_input_field.name.toLowerCase();
    //     var error_message = '<div class="input-field-error-message">Please enter ' + field_name + "</div>";

    //     // Null value
    //     if (required_input_field.value === "") {
    //         required_input_field.style.borderColor = "#D32D2D";
    //         isValid = false;
    //         // eslint-disable-next-line no-undef
    //         show_toast("Please update all mandatory fields");

    //         if (required_input_field.type === "radio" || required_input_field.type === "checkbox") {
    //             // Pass
    //         } else if (required_fields[i].getElementsByClassName("input-field-error-message").length === 0) {
    //             required_fields[i].insertAdjacentHTML("beforeend", error_message);
    //         } else {
    //             if (
    //                 required_fields[i].getElementsByClassName("input-field-validation-message").length !== 0
    //             ) {
    //                 required_fields[i].getElementsByClassName(
    //                     "input-field-validation-message"
    //                 )[0].style.display = "none";
    //             }
    //             required_fields[i].getElementsByClassName("input-field-error-message")[0].style.display =
    //                 "block";
    //         }
    //     }

    //     // Checking valid value
    //     else {
    //         required_input_field.style.borderColor = "#E3E3E3";
    //         // Removing the error message of not filling the input field
    //         if (required_fields[i].getElementsByClassName("input-field-error-message").length !== 0) {
    //             required_fields[i].getElementsByClassName("input-field-error-message")[0].style.display =
    //                 "none";
    //         }

    //         if (required_fields[i].getElementsByClassName("input-field-validation-message").length !== 0) {
    //             required_fields[i].getElementsByClassName("input-field-validation-message")[0].style.display =
    //                 "none";
    //         }

    //         if (required_input_field.type === "email") {
    //             // eslint-disable-next-line no-undef
    //             if (is_valid_email(required_input_field.value) === false) {
    //                 isValid = false;
    //                 const validation_message =
    //                     '<div class="input-field-validation-message">Please enter a valid email address</div>';
    //                 required_input_field.style.borderColor = "#D32D2D";
    //                 // eslint-disable-next-line no-undef
    //                 show_toast("Please update all mandatory fields");

    //                 if (
    //                     required_fields[i].getElementsByClassName("input-field-validation-message").length ===
    //                     0
    //                 ) {
    //                     required_fields[i].insertAdjacentHTML("beforeend", validation_message);
    //                 } else {
    //                     required_fields[i].getElementsByClassName(
    //                         "input-field-validation-message"
    //                     )[0].style.display = "block";
    //                 }
    //             }
    //         } else if (required_input_field.type === "url") {
    //             // eslint-disable-next-line no-undef
    //             if (is_valid_url(required_input_field.value) === false) {
    //                 isValid = false;
    //                 const validation_message =
    //                     '<div class="input-field-validation-message">Please enter a valid url</div>';
    //                 // eslint-disable-next-line no-undef
    //                 show_toast("Please update all mandatory fields");
    //                 required_input_field.style.borderColor = "#D32D2D";

    //                 if (
    //                     required_fields[i].getElementsByClassName("input-field-validation-message").length ===
    //                     0
    //                 ) {
    //                     required_fields[i].insertAdjacentHTML("beforeend", validation_message);
    //                 } else {
    //                     required_fields[i].getElementsByClassName(
    //                         "input-field-validation-message"
    //                     )[0].style.display = "block";
    //                 }
    //             }
    //         } else if (required_input_field.type === "tel") {
    //             // eslint-disable-next-line no-undef
    //             if (is_valid_tel_number(required_input_field.value) === false) {
    //                 isValid = false;
    //                 const validation_message =
    //                     '<div class="input-field-validation-message">Please enter a valid telephone number</div>';
    //                 // eslint-disable-next-line no-undef
    //                 show_toast("Please update all mandatory fields");
    //                 required_input_field.style.borderColor = "#D32D2D";

    //                 if (
    //                     required_fields[i].getElementsByClassName("input-field-validation-message").length ===
    //                     0
    //                 ) {
    //                     required_fields[i].insertAdjacentHTML("beforeend", validation_message);
    //                 } else {
    //                     required_fields[i].getElementsByClassName(
    //                         "input-field-validation-message"
    //                     )[0].style.display = "block";
    //                 }
    //             }
    //         } else if (required_input_field.type === "radio" || required_input_field.type === "checkbox") {
    //             var options = required_fields[i].getElementsByClassName("form-check-input");
    //             var isChecked = false;

    //             for (let j = 0; j < options.length; j++) {
    //                 // Options[j].style.outline = 'none'

    //                 if (options[j].checked) {
    //                     isChecked = true;
    //                 }
    //             }

    //             if (isChecked === false) {
    //                 isValid = false;
    //                 var field_name_checked = required_input_field.name.toLowerCase();
    //                 var select_error_message =
    //                     '<div class="input-field-error-message">Please select ' +
    //                     field_name_checked +
    //                     "</div>";

    //                 if (required_fields[i].getElementsByClassName("input-field-error-message").length === 0) {
    //                     required_fields[i].insertAdjacentHTML("beforeend", select_error_message);
    //                 } else {
    //                     required_fields[i].getElementsByClassName(
    //                         "input-field-error-message"
    //                     )[0].style.display = "block";
    //                 }

    //                 // For(let j=0; j<options.length; j++){
    //                 //   options[j].style.outline = '1px solid #D32D2D'
    //                 // }
    //             }
    //         }
    //     }
    // }

    if (isValid) {
        form.submit();
    }
}
