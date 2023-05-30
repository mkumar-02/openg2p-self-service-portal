const table = $("#newreimbursements");
const tbody = table.find("tbody");
const totalRow = tbody[0].childElementCount;

function addTableSrNo() {
    for (let i = 0; i < totalRow; i++) {
        tbody[0].children[i].firstElementChild.innerText = i + 1;
    }
}

Window.onload = addTableSrNo();
