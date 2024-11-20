class MedicationPagination {
    constructor(listElement) {
        if (!listElement) {
            return;
        }

        this.list = listElement;
        this.currentPage = 1;
        this.itemsPerPage = 3;
        this.totalItems = Array.from(this.list.querySelectorAll('.shop__item'));

        this.list.innerHTML = "";

        this.init();
    }

    init() {
        this.renderCurrentItems();
        this.renderPagination();
        this.addParalax();
    }

    renderCurrentItems() {
        this.list.innerHTML = "";

        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        this.totalItems.slice(startIndex, startIndex + this.itemsPerPage).forEach(item => {
            this.list.appendChild(item);
        });
    }

    renderPagination() {
        const paginationControls = document.querySelector("#pagination-controls");
        paginationControls.innerHTML = "";

        const totalPages = Math.ceil(this.totalItems.length / this.itemsPerPage);
        
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement("button");
            button.classList.add('button', 'pagination__button');
            button.innerText = i;

            const currentI = i;
            button.addEventListener('click', () => {
                this.currentPage = currentI;
                this.renderCurrentItems();
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

    addParalax() {
        const body = document.querySelector('body'), walk = {x: 15, y: 15};

        body.addEventListener('mousemove', (e) => {
            const { clientX, clientY } = e;
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;

            const deltaX = (clientX - centerX) / centerX; 
            const deltaY = (clientY - centerY) / centerY;

            this.totalItems.forEach(item => {
                const intensity = 10;
                const offsetX = -deltaX * intensity;
                const offsetY = -deltaY * intensity;

                item.style.transform = "";

                if (!item.matches(":hover")) {
                    item.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
                }
            });
        });
    }
}


export default MedicationPagination;