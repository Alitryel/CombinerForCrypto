        const searchInput = document.getElementById('searchInput');
        const filterInput = document.getElementById('filterInput');
        const siteSelect = document.getElementById('siteSelect');
        const dataRows = document.querySelectorAll('.data-row');

function applyFilter() {
    const searchQuery = searchInput.value.trim().toLowerCase();
    const filterValue = parseFloat(filterInput.value);
    const selectedSites = Array.from(siteSelect.selectedOptions).map(option => option.value);
    const filterCondition = document.getElementById('filterCondition').checked ? 'lessThan' : 'greaterThan';

    dataRows.forEach(row => {
        const addressCell = row.querySelector('td:first-child');
        const dataCells = row.querySelectorAll('td.data-cell');

        let shouldShowRow = true;

        if (searchQuery && !addressCell.textContent.toLowerCase().includes(searchQuery)) {
            shouldShowRow = false;
        }

        if (selectedSites.length > 0) {
            let anyCellPassesFilter = false;
            dataCells.forEach(cell => {
                const cellValue = parseFloat(cell.textContent.replace('$', ''));
                const cellSite = cell.getAttribute('data-site');
                if (!isNaN(cellValue) && selectedSites.includes(cellSite)) {
                    if ((filterCondition === 'lessThan' && cellValue > filterValue) ||
                        (filterCondition === 'greaterThan' && cellValue < filterValue)) {
                        anyCellPassesFilter = true;
                    }
                }
            });
            if (anyCellPassesFilter) {
                shouldShowRow = false;
            }
        }

        row.style.display = shouldShowRow ? 'table-row' : 'none';
    });
}


        searchInput.addEventListener('input', applyFilter);
        filterInput.addEventListener('input', applyFilter);
        siteSelect.addEventListener('change', applyFilter);

    function downloadCSV() {
        const csvRows = [];

        const headers = ['Address'];
        dataRows[0].querySelectorAll('td.data-cell').forEach(cell => {
            headers.push(cell.getAttribute('data-site'));
        });
        csvRows.push(headers.join(';'));

        dataRows.forEach(row => {
            if (row.style.display !== 'none') {
            const cells = [row.querySelector('td:first-child').textContent];
            row.querySelectorAll('td.data-cell').forEach(cell => {
                const firstValue = cell.textContent;
                const secondValue = cell.nextElementSibling.textContent;
                const combinedValue = `${firstValue} | ${secondValue}`;
                cells.push(combinedValue);
            });
            csvRows.push(cells.join(';'));
            }
        });

        const csvContent = csvRows.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'website_data.csv';
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }