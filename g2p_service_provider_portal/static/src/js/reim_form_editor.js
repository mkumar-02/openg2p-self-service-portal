odoo.define("g2p_service_provider_portal.reim_form_editor", function (require) {
    var FormEditorRegistry = require("website.form_editor_registry");

    FormEditorRegistry.add("apply_for_reimbursement", {
        formFields: [
            {
                type: "char",
                custom: false,
                required: true,
                placeholder: "Enter Voucher Code",
                fillWith: "code",
                name: "code",
                string: "Voucher Code",
            },
            {
                type: "float",
                custom: false,
                required: true,
                placeholder: "Enter Amount",
                fillWith: "initial_amount",
                name: "initial_amount",
                string: "Actual Amount",
            },
            {
                type: "binary",
                custom: true,
                required: true,
                name: "invoice",
                string: "Invoice",
            },
        ],
    });
});
