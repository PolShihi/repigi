class BackgroundAnimation {
    constructor(backgroundElement) {
        if (!backgroundElement) {
            return;
        }

        this.background = backgroundElement;
        this.bottleCount = 50;
        this.bottleSrc = this.background.getAttribute('data-src');
        this.bottles = [];

        this.init();
        this.addSoundAnimation();
    }

    init() {
        for (let i = 0; i < this.bottleCount; i++) {
            const bottle = document.createElement('img');
            bottle.src = this.bottleSrc;
            bottle.classList.add('background__bottle');

            bottle.style.left = `${(i > this.bottleCount / 2 - 1) ? (Math.random() * 30) : (70 + Math.random() * 30)}vw`;
            bottle.style.top = `${Math.random() * 100}vh`;
    
            const size = Math.random() * 30 + 20;
            const initialRotate = Math.random() * 360;
            const initialTop = parseFloat(bottle.style.top) + window.scrollY * (0.1 + (i % 5) * 0.05);
            bottle.style.width = size;
            bottle.style.transform = `translateY(${initialTop}px) rotate(${initialRotate}deg)`;

            this.background.appendChild(bottle);
            this.bottles.push({ element: bottle, rotation: initialRotate });
        }

        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
    
            this.bottles.forEach((bottle, i) => {
                const speed = 0.1 + (i % 5) * 0.05;
                const newTop = parseFloat(bottle.element.style.top) + scrollY * speed;
    

                const rotationSpeed = 0.1 + 0.4 * Math.random();
                bottle.rotation += rotationSpeed;

                bottle.element.style.transform = `translateY(${newTop}px) rotate(${bottle.rotation}deg)`;
            });
        });
    }

    async addSoundAnimation () {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const audioContext = new AudioContext();
            const analyser = audioContext.createAnalyser();
            const microphone = audioContext.createMediaStreamSource(stream);
            const dataArray = new Uint8Array(analyser.frequencyBinCount);
            microphone.connect(analyser);

            const animateBottles = () => {
                analyser.getByteFrequencyData(dataArray);

                const volume = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length;

                this.bottles.forEach(bottle => {
                    bottle.element.style.filter = `blur(${volume / 20}px)`;
                });
    
                requestAnimationFrame(animateBottles);
            }
    
            animateBottles();
        } catch (err) {
            console.error(err);
        }
    }
}


export default BackgroundAnimation;