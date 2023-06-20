const alltable = document.getElementById("allprograms");
const allheadercells = alltable.querySelectorAll("th");
const allRows = Array.from(alltable.querySelectorAll("tbody tr"));
const tbody = alltable.getElementsByTagName("tbody");
const totalRow = tbody[0].children.length;

function addTableSrNo() {
    for (let i = 0; i < totalRow; i++) {
        tbody[0].children[i].firstElementChild.innerText = i + 1;
    }
}

addTableSrNo();
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
const searchInputText = document.getElementById("search-text");
const searchClearText = document.getElementById("search-text-clear");
searchClearText.style.display = "none";

function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const rows = allRows.slice(startIndex, endIndex);
    // Hide all rows
    allRows.forEach((row) => (row.style.display = "none"));
    // Show rows for current page
    rows.forEach((row) => (row.style.display = ""));
}
function renderPageButtons() {
    // Angle bracket for left arrow
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
            currentPage = i;
            showPage(currentPage);
            // Update active class for buttons
            const buttons = pageButtonsContainer.querySelectorAll("button");
            buttons.forEach((btn) => {
                btn.classList.remove("active");
                if (Number(btn.textContent) === currentPage) {
                    btn.classList.add("active");
                }
            });
            // Enable/disable prev and next buttons based on current page
            prevButton.disabled = currentPage === 1;
            nextButton.disabled = currentPage === totalPages;
        });

        pageButtonsContainer.appendChild(button);
    }

    // Angular bracket for right arrow

    nextButton.classList.add("next-button");
    nextButton.addEventListener("click", function () {
        currentPage++;
        showPage(currentPage);
        const buttons = pageButtonsContainer.querySelectorAll("button");
        buttons.forEach((button) => {
            button.classList.remove("active");
            if (Number(button.textContent) === currentPage) {
                button.classList.add("active");
            }
        });
        prevButton.disabled = false;
        nextButton.disabled = currentPage === totalPages;
    });
    pageButtonsContainer.appendChild(nextButton);

    // Disable pagination if no records or only one page
    if (totalPages <= 1 || allRows.length === 0) {
        prevButton.disabled = true;
        nextButton.disabled = true;
    } else {
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }
}

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
    currentPage = 1;
    showPage(currentPage);
    const buttons = pageButtonsContainer.querySelectorAll("button");
    buttons.forEach((button) => {
        button.classList.remove("active");
        if (Number(button.textContent) === currentPage) {
            button.classList.add("active");
        }
    });
    prevButton.disabled = true;
    // Enable next button when prev button is clicked
    nextButton.disabled = false;
    // Hide search clear button
    searchClearText.style.display = "none";
});

document.addEventListener("click", function (event) {
    if (event.target !== searchInputText && event.target !== searchClearText) {
        searchClearText.style.display = searchInputText.value ? "block" : "none";
    }
});
showPage(currentPage);
renderPageButtons();
