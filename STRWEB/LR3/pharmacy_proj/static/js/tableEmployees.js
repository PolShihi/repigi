class EmployeeTable {
    constructor(tableElement) {
        if (!tableElement) {
            return;
        }

        this.table = tableElement;
        this.tbody = this.table.querySelector("tbody");
        this.currentPage = 1;
        this.itemsPerPage = 3;
        this.totalRows = Array.from(this.table.querySelectorAll('.contacts__item'));
        this.selectedRows = [...this.totalRows];
        this.sortOrder = {};

        this.tbody.innerHTML = "";

        this.init();
    }

    init() {
        this.setupAddEmployeeForm();
        this.setupBonusButton();
        this.addRowSelectionListener();
        this.addSortingListeners();
        this.addFilteringListeners();
        this.renderCurrentRows();
        this.renderPagination();
    }

    renderCurrentRows() {
        this.tbody.innerHTML = "";

        document.querySelector('.pill').style.display = 'block';
        document.querySelectorAll('.contacts *').forEach((e) => e.disabled = true);

        setTimeout(() => {
            document.querySelector('.pill').style.display = 'none';
            document.querySelectorAll('.contacts *').forEach((e) => e.disabled = false);

            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            this.selectedRows.slice(startIndex, startIndex + this.itemsPerPage).forEach(row => {
            this.tbody.appendChild(row);
            });
        }, 1000);
    }

    setupBonusButton() {
        const bonusButton = document.querySelector("#bonus-button");

        bonusButton.addEventListener("click", () => {
            const selectedEmployees = this.totalRows
                .filter(row => row.querySelector(".contacts__item-checkbox input").checked)
                .map(row => {
                    row.querySelector(".contacts__item-checkbox input").checked = false;
                    return row.querySelector(".contacts__item-name").innerText;});

            if (selectedEmployees.length > 0) {
                const message = `Premiate the following employees: ${selectedEmployees.join(", ")}`;
                document.querySelector("#bonus-message").innerText = message;
            }
        });
    }

    renderPagination() {
        const paginationControls = document.querySelector("#pagination-controls");
        paginationControls.innerHTML = "";

        const totalPages = Math.ceil(this.selectedRows.length / this.itemsPerPage);
        
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement("button");
            button.classList.add('button', 'pagination__button');
            button.innerText = i;

            const currentI = i;
            button.addEventListener('click', () => {
                this.currentPage = currentI;
                this.renderCurrentRows();
                this.highlightActivePage(currentI);
            });

            paginationControls.appendChild(button);
        }

        this.highlightActivePage(this.currentPage);
    }

    highlightActivePage(page) {
        const buttons = document.querySelectorAll("#pagination-controls button");
        buttons.forEach((button, index) => {
            button.classList.toggle("pagination__button_active", index + 1 === page);
        });
    }

    resetSorting() {
        this.table.querySelectorAll("thead th span").forEach((span) => span?.remove());
    }

    addSortingListeners() {
        const headers = this.table.querySelectorAll("thead th");
        headers.forEach((header, columnIndex) => {
            if (columnIndex < 2) {
                header.style.cursor = "default";
                return;
            }

            header.addEventListener("click", () => this.sortByColumn(columnIndex, header));
        });
    }

    sortByColumn(columnIndex, header) {
        const isAscending = !this.sortOrder[columnIndex];
        this.sortOrder = { [columnIndex]: isAscending };
        const icon = isAscending ? "▲" : "▼";

        this.selectedRows.sort((rowA, rowB) => {
            const cellA = rowA.children[columnIndex].innerText.trim().toLowerCase();
            const cellB = rowB.children[columnIndex].innerText.trim().toLowerCase();

            if (cellA < cellB) return isAscending ? -1 : 1;
            if (cellA > cellB) return isAscending ? 1 : -1;
            return 0;
        });

        this.table.querySelectorAll("thead th span").forEach((span) => span?.remove());
        const span = document.createElement("span");
        span.innerText = ` ${icon}`;
        header.appendChild(span);

        this.renderCurrentRows();
    }

    addFilteringListeners() {
        const filterInput = document.querySelector("#filter-input");
        const filterButton = document.querySelector("#filter-button");

        filterButton.addEventListener("click", () => {
            const filterText = filterInput.value.trim().toLowerCase();
            this.selectedRows = this.totalRows.filter((row) =>
                Array.from(row.children).some((cell) => {
                    console.log(cell.innerText);
                    console.log(cell.innerText.toLowerCase());
                    console.log(cell.innerText.toLowerCase().includes(filterText));
                    return cell.innerText.toLowerCase().includes(filterText);
                }
                )
            );

            this.resetSorting();
            this.currentPage = 1;
            this.renderCurrentRows();
            this.renderPagination();
        });
    }

    addRowSelectionListener() {
        this.totalRows.forEach((row) => {
            row.addEventListener("click", (e) => {
                if (e.target.matches('input')){
                    return;
                }

                const infoBlock = document.querySelector("#selected-row-info");
                
                infoBlock.querySelector(".contacts__details-image").setAttribute("src", row.querySelector('.contacts__item-image img').getAttribute("src"));
                infoBlock.querySelector(".contacts__details-name").textContent = row.querySelector('.contacts__item-name').textContent;
                infoBlock.querySelector(".contacts__details-email").textContent = `(${row.querySelector('.contacts__item-email').textContent})`;
                infoBlock.querySelector(".contacts__details-phone-value").textContent = row.querySelector('.contacts__item-phone').textContent;
                infoBlock.querySelector(".contacts__details-position-value").textContent = row.querySelector('.contacts__item-position').textContent;
                
                infoBlock.style.display = "block";
            });
        });
    }

    setupAddEmployeeForm() {
        const showButton = document.querySelector("#show-employee-form");
        const form = document.querySelector("#employee-form");
        const submitButton = form.querySelector("#add-to-table-button");

        const nameInput = form.querySelector('[name="name"]');
        const photoInput = form.querySelector('[name="photo"]');
        const urlInput = form.querySelector('[name="url"]');
        const emailInput = form.querySelector('[name="email"]');
        const phoneInput = form.querySelector('[name="phone"]');
        const positionInput = form.querySelector('[name="position"]');

        showButton.addEventListener("click", () => {
            if (form.classList.toggle('hidden')) {
                showButton.textContent = "Show form";
            } else {
                showButton.textContent = "Hide form";
            }
        });

        const validateForm = () => {
            const urlValid = this.validateURL(urlInput.value);
            const phoneValid = this.validatePhone(phoneInput.value);

            document.querySelector("#url-validation").innerText = urlValid ? "" : "Invalid URL.";
            document.querySelector("#phone-validation").innerText = phoneValid ? "" : "Invalid phone number.";

            urlInput.classList.toggle("invalid", !urlValid);
            phoneInput.classList.toggle("invalid", !phoneValid);

            if (urlValid && phoneValid && nameInput.checkValidity() && photoInput.checkValidity() && emailInput.checkValidity() && positionInput.checkValidity()) {
                submitButton.style.display = "block";
            } else {
                submitButton.style.display = "none";
            }
        };

        validateForm();

        urlInput.addEventListener("blur", validateForm);
        phoneInput.addEventListener("blur", validateForm);
        photoInput.addEventListener("blur", validateForm);
        nameInput.addEventListener("blur", validateForm);
        emailInput.addEventListener("blur", validateForm);
        positionInput.addEventListener("blur", validateForm);

        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const formData = new FormData(form);

            fetch(form.action, {
                method: "POST",
                body: formData,
            }).then((response) => {
                if (!response.ok) {
                    return response.json().then((error) => {
                        throw new Error(error.error || "Failed to add employee.");
                    });
                }

                console.log("Success");
            }).catch((err) => {
                console.error("Error submitting form:", err);
            });


            const name = formData.get("name");
            const photoFile = formData.get("photo");
            const email = formData.get("email");
            const phone = formData.get("phone");
            const position = formData.get("position");

            const photoURL = photoFile ? URL.createObjectURL(photoFile) : "";

            const newRow = this.createEmployeeRow(name, photoURL, email, phone, position);
            this.totalRows.push(newRow);
            this.selectedRows = this.totalRows;

            this.currentPage = 1;
            this.resetSorting();
            this.renderCurrentRows();
            this.renderPagination();

            form.reset();
        });
    }

    validateURL(url) {
        const regex = /^(https?:\/\/)([a-zA-Z0-9.-\/]+)\.(php|html)$/;
        return regex.test(url);
    }

    validatePhone(phone) {
        const regex = /^(8|\+?375)\s*(\(?\d{2,3}\)?)\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
        return regex.test(phone);
    }

    createEmployeeRow(name, photo, email, phone, position) {
        const row = document.createElement("tr");
        row.classList.add("contacts__item");

        row.innerHTML = `
            <td class="contacts__item-checkbox"><input type="checkbox"></td>
            <td class="contacts__item-image"><img src="${photo}" alt="Employee Photo"></td>
            <td class="contacts__item-name">${name}</td>
            <td class="contacts__item-email">${email}</td>
            <td class="contacts__item-phone">${phone}</td>
            <td class="contacts__item-position">${position}</td>
        `;

        row.addEventListener("click", (e) => {
            if (e.target.matches('input')){
                return;
            }

            const infoBlock = document.querySelector("#selected-row-info");
            
            infoBlock.querySelector(".contacts__details-image").setAttribute("src", row.querySelector('.contacts__item-image img').getAttribute("src"));
            infoBlock.querySelector(".contacts__details-name").textContent = row.querySelector('.contacts__item-name').textContent;
            infoBlock.querySelector(".contacts__details-email").textContent = `(${row.querySelector('.contacts__item-email').textContent})`;
            infoBlock.querySelector(".contacts__details-phone-value").textContent = row.querySelector('.contacts__item-phone').textContent;
            infoBlock.querySelector(".contacts__details-position-value").textContent = row.querySelector('.contacts__item-position').textContent;
            
            infoBlock.style.display = "block";
        });

        return row;
    }
}


export default EmployeeTable;