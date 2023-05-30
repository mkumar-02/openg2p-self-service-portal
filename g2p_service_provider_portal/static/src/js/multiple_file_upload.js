var remove_btn_clicked = false;

// eslint-disable-next-line no-unused-vars,complexity
function upload_documents() {
    var input_field = $("#statement_of_account");
    var document_container = $("#multiple-file-upload");

    if (remove_btn_clicked) {
        remove_btn_clicked = false;
    } else {
        document_container.click = input_field.trigger("click");
    }
}

// eslint-disable-next-line no-unused-vars,complexity
function display_uploaded_files() {
    var dt = new DataTransfer();
    var input_field = document.getElementById("statement_of_account");
    document.getElementById("multiple-file-upload").innerHTML = "";

    for (let i = 0; i < input_field.files.length; i++) {
        var fileBloc = document.createElement("span");
        fileBloc.classList.add("file-block");

        var fileName = document.createElement("span");
        fileName.classList.add("name");
        fileName.textContent = input_field.files.item(i).name;

        var del = document.createElement("span");
        del.classList.add("file-delete");

        var del_button = document.createElement("span");
        del_button.textContent = "+";

        del.appendChild(del_button);
        fileBloc.appendChild(del);

        fileBloc.append(fileName);
        document.getElementById("multiple-file-upload").append(fileBloc);

        dt.items.add(input_field.files[i]);
    }

    input_field.files = dt.files;

    $("span.file-delete").click(function (e) {
        if (input_field.files.length === 1) {
            document.getElementById("multiple-file-upload").innerHTML =
                '<i class="fa fa-upload upload-icon" style="color: #704880; font-size: x-large;"></i><p style="margin: 0px">Upload Document or drag and drop your document(s) here</p>';
        }
        remove_btn_clicked = true;
        const name = e.currentTarget.nextElementSibling.textContent;
        $(e.currentTarget).parent().remove();
        for (let i = 0; i < dt.items.length; i++) {
            if (name === dt.items[i].getAsFile().name) {
                dt.items.remove(i);
                continue;
            }
        }
        document.getElementById("statement_of_account").files = dt.files;
    });
}
