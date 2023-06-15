// eslint-disable-next-line no-unused-vars,complexity
function reimbursementFormSubmitAction() {
    var form = $("#reimbursement-form");

    var program_id = $("#program_submit_id");
    form[0].action = `/serviceprovider/claim/${program_id[0].getAttribute("program")}`;

    var fileUploadSize = program_id[0].getAttribute("file-size");
    var isValid = true;

    // TODO: validations

    var modal = $("#SubmitModal");
    var requiredFields = $(".s_website_form_required");
    var inputFields = requiredFields.find("input");

    for (let i = 0; i < requiredFields.length; i++) {
        inputFields[i].style.borderColor = "#E3E3E3";
        if (inputFields[i].value === "") {
            isValid = false;
            modal[0].click(close);
            // eslint-disable-next-line no-undef
            showToast("Please update all mandatory fields");
            inputFields[i].style.borderColor = "#DE514C";
        }
    }

    if (isValid) {
        // eslint-disable-next-line no-undef
        if (isFileAllowed(fileUploadSize)) {
            form.submit();
        } else {
            modal[0].click(close);
        }
    }
}
