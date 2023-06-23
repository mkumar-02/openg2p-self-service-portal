const table = document.getElementById("myprograms");
const headercells = table.querySelectorAll("th");
const tbody = table.getElementsByTagName("tbody");
const totalRow = tbody[0].children.length;

function addTableSrNo() {
    for (let i = 0; i < totalRow; i++) {
        tbody[0].children[i].firstElementChild.innerText = i + 1;
    }
}

addTableSrNo();

headercells.forEach(function (th) {
    // Default sort order
    let sortOrder = "asc";

    th.addEventListener("click", function () {
        const columnIndex = th.cellIndex;
        const rows = Array.from(table.rows).slice(1);
        // Determine the data type for this column

        let dataType = "text";
        const firstRow = rows[0];
        const firstCell = firstRow.cells[columnIndex];
        if (firstCell) {
            const cellContent = firstCell.innerText.trim();
            if (/^\d+$/.test(cellContent)) {
                dataType = "number";
            } else if (Date.parse(cellContent)) {
                dataType = "date";
            }
        }

        rows.sort(function (a, b) {
            let aCellValue = a.cells[columnIndex].innerText.trim();
            let bCellValue = b.cells[columnIndex].innerText.trim();

            if (dataType === "number") {
                aCellValue = parseFloat(aCellValue);
                bCellValue = parseFloat(bCellValue);
            } else if (dataType === "date") {
                aCellValue = new Date(aCellValue);
                bCellValue = new Date(bCellValue);
            }

            let comparison = 0;
            if (aCellValue > bCellValue) {
                comparison = 1;
            } else if (aCellValue < bCellValue) {
                comparison = -1;
            }

            if (sortOrder === "desc") {
                comparison *= -1;
            }

            return comparison;
        });

        sortOrder = sortOrder === "asc" ? "desc" : "asc";

        table.tBodies[0].append(...rows);
    });
});

const searchInput = document.getElementById("search-input");
const searchClear = document.getElementById("search-clear");
searchClear.style.display = "none";

searchInput.addEventListener("input", function (event) {
    const searchValue = event.target.value.toLowerCase();

    for (let i = 1; i < table.rows.length; i++) {
        const row = table.rows[i];
        const cells = row.cells;
        const cell = cells[1];

        if (cell.innerText.toLowerCase().indexOf(searchValue) > -1) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }

    if (searchValue || searchInput === document.activeElement) {
        searchClear.style.display = "block";
    } else {
        searchClear.style.display = "none";
    }
});

searchInput.addEventListener("focusout", function () {
    if (!searchInput.value) {
        searchClear.style.display = "none";
    }
});

searchClear.addEventListener("click", function () {
    searchInput.value = "";
    for (let i = 1; i < table.rows.length; i++) {
        const row = table.rows[i];
        row.style.display = "";
    }
    searchClear.style.display = "none";
});

document.addEventListener("click", function (event) {
    if (event.target !== searchInput && event.target !== searchClear) {
        searchClear.style.display = searchInput.value ? "block" : "none";
    }
});
