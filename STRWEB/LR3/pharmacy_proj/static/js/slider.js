class Slider {
    constructor(slider, options = {}) {
        if (!slider) {
            return;
        }

        this.slider = slider;
        this.slidesContainer = slider?.querySelector('.slider__slides');
        this.slideElements = slider?.querySelectorAll('.slider__slide');
        this.currentIndex = 0;
        this.loop = Boolean(options.loop ?? true);
        this.navs = Boolean(options.navs ?? true);
        this.pags = Boolean(options.pags ?? true);
        this.auto = Boolean(options.auto ?? true);
        this.stopMouseHover = Boolean(options.stopMouseHover ?? true);
        this.delay = Number(options.delay ?? 5);
        this.timer = null;

        this.init();
    }

    init() {
        if (this.navs) {
            this.slider.querySelector('.slider__prev').addEventListener('click', () => this.prev());
            this.slider.querySelector('.slider__next').addEventListener('click', () => this.next());
        } else {
            this.slider.querySelector('.slider__prev').style.cssText = "display: none;";
            this.slider.querySelector('.slider__next').style.cssText = "display: none;";
        }

        if (this.pags) {
            this.createPagination();
        }

        if (this.auto) {
            this.startAutoSlide();

            if (this.stopMouseHover) {
                this.slider.addEventListener('mouseenter', () => {this.stopAutoSlide(); console.log("start");});
                this.slider.addEventListener('mouseleave', () => {this.startAutoSlide(); console.log("stop");});
            }
        }

        this.updateSlide();
    }

    createPagination() {
        const paginationElement = this.slider.querySelector('.slider__pagination');

        this.slideElements.forEach((_, index) => {
            const pageElement = document.createElement('div');
            pageElement.addEventListener('click', () => this.goToSlide(index));
            paginationElement.appendChild(pageElement);
        });
    }

    updateSlide() {
        this.slidesContainer.style.transform = `translateX(${-this.currentIndex * 100}%)`;

        this.updateCurrentSlideText();

        if (this.pags) {
            const pageElements = this.slider.querySelectorAll('.slider__pagination div');

            pageElements.forEach((pageElement, index) => {
                pageElement.classList.toggle('active', index === this.currentIndex);
            });
        }
    }

    updateCurrentSlideText() {
        const counterText = this.slider.querySelector('.slider__counter');
        counterText.textContent = `${this.currentIndex + 1}/${this.slideElements.length}`;
    }

    goToSlide(index) {
        this.currentIndex = index;
        this.updateSlide();
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % this.slideElements.length;

        if (!this.loop && this.currentIndex === 0) {
            this.currentIndex = this.slideElements.length - 1;
        }

        this.updateSlide();
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.slideElements.length) % this.slideElements.length;

        if (!this.loop && this.currentIndex === this.slideElements.length - 1) {
            this.currentIndex = 0;
        }

        this.updateSlide();
    }

    startAutoSlide() {
        this.timer = setInterval(() => this.next(), this.delay * 1000);
    }

    stopAutoSlide() {
        clearInterval(this.timer);
    }
}

export default Slider;