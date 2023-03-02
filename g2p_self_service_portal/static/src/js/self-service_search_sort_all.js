const alltable = document.getElementById("allprograms");
const allheadercells = alltable.querySelectorAll("th");

allheadercells.forEach(function (th) {
    let sortOrder = "asc"; // Default sort order

    th.addEventListener("click", function () {
        const columnIndex = th.cellIndex;
        const rows = Array.from(alltable.rows).slice(1);

        rows.sort(function (a, b) {
            const aCellValue = a.cells[columnIndex].innerText;
            const bCellValue = b.cells[columnIndex].innerText;

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

        alltable.tBodies[0].append(...rows);
    });
});

const searchInputText = document.getElementById("search-text");
const searchClearText = document.getElementById("search-text-clear");
searchClearText.style.display = "none";

searchInputText.addEventListener("input", function (event) {
    const searchValue = event.target.value.toLowerCase();

    for (let i = 1; i < alltable.rows.length; i++) {
        const row = alltable.rows[i];
        const cells = row.cells;

        let rowMatch = false;

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];

            if (cell.innerText.toLowerCase().indexOf(searchValue) > -1) {
                rowMatch = true;
                break;
            }
        }

        if (rowMatch) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }

    if (searchValue && searchInputText === document.activeElement) {
        searchClearText.style.display = "block";
    } else {
        searchClearText.style.display = "none";
    }
});

searchInputText.addEventListener("focus", function () {
    if (searchInputText.value && searchInputText === document.activeElement) {
        searchClearText.style.display = "block";
    }
});

searchInputText.addEventListener("blur", function () {
    setTimeout(function () {
        searchClearText.style.display = "none";
    }, 200);
});

searchClearText.addEventListener("click", function () {
    searchInputText.value = "";
    for (let i = 1; i < alltable.rows.length; i++) {
        const row = alltable.rows[i];
        row.style.display = "";
    }
    searchClearText.style.display = "none";
});

document.addEventListener("click", function (event) {
    if (event.target !== searchInputText && event.target !== searchClearText) {
        searchClearText.style.display = "none";
    }
});
