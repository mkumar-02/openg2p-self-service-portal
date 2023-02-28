
const table = document.getElementById("myprograms");
const headercells = table.querySelectorAll("th");

headercells.forEach(function(th) {
  let sortOrder = "asc"; // default sort order

  th.addEventListener("click", function() {
    const columnIndex = th.cellIndex;
    const rows = Array.from(table.rows).slice(1);

    rows.sort(function(a, b) {
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

    table.tBodies[0].append(...rows);
  });
});


const searchInput = document.getElementById("search-input");
const searchClear = document.getElementById("search-clear");
searchClear.style.display = "none";

searchInput.addEventListener("input", function(event) {
  const searchValue = event.target.value.toLowerCase();
  
  for (let i = 1; i < table.rows.length; i++) {
    const row = table.rows[i];
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

  if (searchValue && searchInput === document.activeElement) {
    searchClear.style.display = "block";
  } else {
    searchClear.style.display = "none";
  }
});

searchInput.addEventListener("focus", function() {
  if (searchInput.value && searchInput === document.activeElement) {
    searchClear.style.display = "block";
  }
});

searchInput.addEventListener("blur", function() {
  setTimeout(function() {
    searchClear.style.display = "none";
  }, 200);
});

searchClear.addEventListener("click", function() {
  searchInput.value = "";
  for (let i = 1; i < table.rows.length; i++) {
    const row = table.rows[i];
    row.style.display = "";
  }
  searchClear.style.display = "none";
});

document.addEventListener("click", function(event) {
  if (event.target !== searchInput && event.target !== searchClear) {
    searchClear.style.display = "none";
  }
});


