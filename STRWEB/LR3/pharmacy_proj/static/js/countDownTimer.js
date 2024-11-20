class CountdownTimer {
    constructor(duration, displayElement) {
        this.duration = duration;
        this.displayElement = displayElement;
        this.remainingTime = sessionStorage.getItem('remainingTime') 
            ? parseInt(sessionStorage.getItem('remainingTime'), 10) 
            : duration;

        if (!sessionStorage.getItem('remainingTime')) {
            sessionStorage.setItem('remainingTime', this.remainingTime);
        }

        this.start();
    }

    start() {
        this.update()
        this.countdownInterval = setInterval(() => this.update(), 1000);
    }

    update() {
        if (this.remainingTime > 0) {
            this.remainingTime -= 1000;
            sessionStorage.setItem('remainingTime', this.remainingTime);
            this.updateDisplay();
        } else {
            if (this.displayElement) {
                this.displayElement.textContent = "Время вышло!";
            }

            clearInterval(this.countdownInterval);
        }
    }

    updateDisplay() {

        if (!this.displayElement) {
            return;
        }

        const hours = Math.floor(this.remainingTime / (1000 * 60 * 60));
        const minutes = Math.floor((this.remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((this.remainingTime % (1000 * 60)) / 1000);

        this.displayElement.textContent = 
            String(hours).padStart(2, '0') + ':' + 
            String(minutes).padStart(2, '0') + ':' + 
            String(seconds).padStart(2, '0');
    }
}

export default CountdownTimer;