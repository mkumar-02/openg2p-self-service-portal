// TODO: The following function is part if selfservice portal module too,
// reuse from there.
// eslint-disable-next-line no-unused-vars,complexity
function reimbursement_form_submit_action() {
    var form = $("#reimbursement-form");

    var program_id = $("#program_submit_id");
    form[0].action = `/serviceprovider/claim/${program_id[0].getAttribute("program")}`;

    var isValid = true;

    // TODO: validations

    if (isValid) {
        form.submit();
    }
}
