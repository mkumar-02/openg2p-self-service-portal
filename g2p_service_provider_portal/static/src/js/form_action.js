var voucherDetails = [];

fetch("/get_voucher_codes")
    .then(function (response) {
        if (response.ok) {
            return response.json();
        }
    })
    .then(function (data) {
        if (data) {
            voucherDetails = data;
        }
    });

// eslint-disable-next-line no-unused-vars,complexity
function reimbursementFormSubmitAction() {
    var form = $("#reimbursement-form");
    var voucherInputField = $("#voucher_code");
    var isValid = true;
    var isValidVoucher = false;
    var program_id = $("#program_submit_id");
    var fileUploadSize = program_id[0].getAttribute("file-size");
    var beneficiayName = program_id[0].getAttribute("beneficiary");

    form[0].action = `/serviceprovider/claim/${program_id[0].getAttribute("program")}`;

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
        } else {
            for (let j = 0; j < voucherDetails.length; j++) {
                if (
                    voucherDetails[j].beneficiary_name === beneficiayName &&
                    voucherDetails[j].code === voucherInputField[0].value
                ) {
                    isValidVoucher = true;
                }
            }
        }
    }

    if (!isValidVoucher) {
        isValid = false;
        modal[0].click(close);
        // eslint-disable-next-line no-undef
        showToast("Please enter a valid voucher code");
        voucherInputField[0].style.borderColor = "#DE514C";
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
