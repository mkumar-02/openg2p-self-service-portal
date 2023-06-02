const table = document.getElementById("newreimbursements");
const tbody = table.getElementsByTagName("tbody");
// TODO: Remove the childElementCount variable
const totalRow = tbody[0].children.length;

table.id = "allprograms";

function addTableSrNo() {
    for (let i = 0; i < totalRow; i++) {
        tbody[0].children[i].firstElementChild.innerText = i + 1;
    }
}

// TODO: remove the onload method
Window.onload = addTableSrNo();
