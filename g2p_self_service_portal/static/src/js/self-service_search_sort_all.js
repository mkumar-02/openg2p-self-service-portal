const alltable = document.getElementById("allprograms");
const allheadercells = alltable.querySelectorAll("th");
const allRows = Array.from(alltable.tBodies[0].rows);

console.log(allRows);
allheadercells.forEach(function (th) {
    // Default sort order
    let sortOrder = "asc";

    th.addEventListener("click", function () {
        const columnIndex = th.cellIndex;

        allRows.sort(function (a, b) {
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
        allRows.forEach(function (row) {
            alltable.tBodies[0].appendChild(row);
        });
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
        const cell = cells[1];

        if (cell.innerText.toLowerCase().indexOf(searchValue) > -1) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }

    if (searchValue || searchInputText === document.activeElement) {
        searchClearText.style.display = "block";
    } else {
        searchClearText.style.display = "none";
    }
});

searchClearText.addEventListener("click", function () {
    searchInputText.value = "";
    allRows.forEach(function (row) {
        row.style.display = "";
    });
    searchClearText.style.display = "none";
});

document.addEventListener("click", function (event) {
    if (event.target !== searchInputText && event.target !== searchClearText) {
        searchClearText.style.display = searchInputText.value ? "block" : "none";
    }
});

const itemsPerPage = 7;
let currentPage = 1;
const totalPages = Math.ceil(allRows.length / itemsPerPage);
const pageButtonsContainer = document.getElementById("page-buttons");
pageButtonsContainer.innerHTML = "";

// Add previous page button
const prevButton = document.createElement("button");
prevButton.innerHTML = '<i class="fa fa-angle-left"></i>';

const nextButton = document.createElement("button");
nextButton.innerHTML = '<i class="fa fa-angle-right"></i>';

// Add Next page button
function showPage(page) {
    const rows = allRows.slice((page - 1) * itemsPerPage, page * itemsPerPage);

    // Hide all rows
    allRows.forEach((row) => (row.style.display = "none"));

    // Show rows for current page
    rows.forEach((row) => (row.style.display = ""));
}

function renderPageButtons() {
    // Angle bracket for left arrow
    prevButton.disabled = true;
    if (currentPage > 1) {
        prevButton.disabled = false;
    }
    prevButton.addEventListener("click", function () {
        currentPage--;
        showPage(currentPage);
        // Update active class for buttons
        const buttons = pageButtonsContainer.querySelectorAll("button");
        buttons.forEach((button) => {
            button.classList.remove("active");
            if (Number(button.textContent) === currentPage) {
                button.classList.add("active");
            }
        });
        // Disable prev button on first page
        if (currentPage === 1) {
            prevButton.disabled = true;
        }
        // Enable next button when prev button is clicked

        nextButton.disabled = false;
    });
    pageButtonsContainer.appendChild(prevButton);

    // Add page buttons
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("button");
        button.textContent = i;
        if (i === currentPage) {
            button.classList.add("active");
        }

        button.addEventListener("click", function () {
            currentPage = String(i);
            showPage(currentPage);
            // Update active class for buttons
            const buttons = pageButtonsContainer.querySelectorAll("button");
            buttons.forEach((btn) => {
                btn.classList.remove("active");
                if (btn.textContent === currentPage) {
                    btn.classList.add("active");
                }
            });
            // Enable/disable prev and next buttons based on current page
            if (currentPage === 1) {
                prevButton.disabled = true;
            } else {
                prevButton.disabled = false;
            }
            if (currentPage === totalPages) {
                nextButton.disabled = true;
            } else {
                nextButton.disabled = false;
            }
        });

        pageButtonsContainer.appendChild(button);
    }

    // Angular bracket for right arrow
    nextButton.disabled = true;
    if (currentPage < totalPages) {
        nextButton.disabled = false;
    }
    nextButton.classList.add("next-button");
    nextButton.addEventListener("click", function () {
        currentPage++;
        showPage(currentPage);
        // Update active class for buttons
        const buttons = pageButtonsContainer.querySelectorAll("button");
        buttons.forEach((button) => {
            button.classList.remove("active");
            if (Number(button.textContent) === currentPage) {
                button.classList.add("active");
            }
        });
        // Disable next button on last page
        if (currentPage === totalPages) {
            nextButton.disabled = true;
        }
        // Enable prev button when next button is clicked
        prevButton.disabled = false;
    });
    pageButtonsContainer.appendChild(nextButton);
}

// Show first page by default
showPage(currentPage);
renderPageButtons();
