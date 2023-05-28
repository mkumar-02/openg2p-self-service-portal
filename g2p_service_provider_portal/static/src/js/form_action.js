// eslint-disable-next-line no-unused-vars,complexity
function reimbursement_form_submit_action() {
    var form = $("#reimbursement-form");

    var program_id = $("#program_submit_id");
    form[0].action = `/serviceprovider/claim/${program_id[0].getAttribute("program")}`;

    var isValid = true;

    // TODO: validations

    var modal = $("#SubmitModal");

    for (let i = 0; i < 4; i++) {
        form[0][i].style.borderColor = "#E3E3E3";
        if (form[0][i].value === "") {
            isValid = false;
            modal[0].click(close);
            show_toast("Please update all mandatory fields");
            form[0][i].style.borderColor = "#DE514C";
        }
    }

    if (isValid) {
        form.submit();
    }
}
