document.addEventListener('DOMContentLoaded', () => {
    // Add event listener to handle real-time changes for DELETE checkboxes
    document.querySelectorAll('input[name$="-DELETE"]').forEach((checkbox) => {
        checkbox.addEventListener('change', (event) => {
            const formsetEntry = checkbox.closest('.formset-entry');
            const formFields = formsetEntry.querySelectorAll('input, select, textarea');
            const isChecked = event.target.checked;

            // Disable or enable fields based on the checkbox state
            formFields.forEach(field => {
                if (field !== event.target) {
                    field.disabled = isChecked;
                }
            });
        });
    });

    // Prevent user entering more than necessary digits than allowed and set cursor correctly
    const numberInputs = document.querySelectorAll('input[type="number"]');

    numberInputs.forEach(input => {
        const fieldName = input.name;

        input.addEventListener('input', (event) => {
            let value = event.target.value;

            const cursorPosition = event.target.selectionStart;

            let newValue;

            if (fieldName.includes('price')) {
                let parts = value.split('.');
                if (parts[0].length > 3) {
                    parts[0] = parts[0].slice(0, 3);
                }
                if (parts.length > 1) {
                    parts[1] = parts[1].slice(0, 2); // Restrict to 2 decimal places
                }
                newValue = parts.join('.');
            } else if (fieldName.includes('stock')) {
                // Allow only integers, no decimal point
                newValue = value.replace(/[^0-9]/g, ''); // Remove all non-numeric characters
                if (newValue.length > 3) {
                    newValue = newValue.slice(0, 3); // Restrict to 3 digits
                }
            } else {
                // Default behavior for other fields
                newValue = value;
            }

            if (newValue !== value) {
                event.target.value = newValue;

                // Restore cursor position
                const adjustment = value.length - newValue.length;
                const newCursorPosition = Math.max(cursorPosition - adjustment, 0);
                event.target.setSelectionRange(newCursorPosition, newCursorPosition);
            }
        });

        // Prevent "-" at the keypress/keydown level for price fields
        if (fieldName.includes('price')) {
            input.addEventListener('keydown', (event) => {
                if (event.key === '-') {
                    event.preventDefault(); // Block the "-" key
                }
            });
        }

        // Prevent "." and "-" at the keypress/keydown level for stock fields
        if (fieldName.includes('stock')) {
            input.addEventListener('keydown', (event) => {
                if (event.key === '.' || event.key === '-') {
                    event.preventDefault(); // Block the "." key
                }
            });
        }
    });

    // Quantity handling
    const quantityInputs = document.querySelectorAll('input[name*="quantity"]');

    quantityInputs.forEach(input => {
        input.addEventListener('input', (event) => {
            const max = parseInt(input.getAttribute('max'), 10);
            const value = parseInt(event.target.value, 10);

            // Enforce range
            if (value > max) {
                event.target.value = max;
                event.target.setSelectionRange(String(max).length, String(max).length); // Adjust cursor position
            } else if (value < 1 || isNaN(value)) {
                event.target.value = 1;
                event.target.setSelectionRange(1, 1);
            }
        });

        // Prevent "-" or "." during typing for quantity fields
        input.addEventListener('keydown', (event) => {
            if (event.key === '.' || event.key === '-' || event.key === 'e') {
                event.preventDefault();
            }
        });
    });

    // Pagination: remember scroll position
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('page')) {
        const paginationDiv = document.querySelector('.pagination');
        if (paginationDiv) {
            // console.log("Pagination element found, scrolling...");
            requestAnimationFrame(() => {
                paginationDiv.scrollIntoView({ behavior: 'smooth' });
            });
        }
    }
});
