class StyleController {
    constructor(container) {
        if (!container) {
            return;
        }

        this.container = container;
        this.createControls();
    }

    rgbToHex(rgb) {
        const rgbValues = rgb.match(/\d+/g);
        
        const hexValues = rgbValues.map(value => {
            const hex = parseInt(value).toString(16);
            return hex.padStart(2, '0');
        });
    
        return `#${hexValues.join('')}`;
    }

    createControls() {
        const fontSizeContainer = document.createElement('div');
        
        const fontSizeLabel = document.createElement('label');
        fontSizeLabel.textContent = 'Размер шрифта:';
        fontSizeContainer.appendChild(fontSizeLabel);

        const fontSizeInput = document.createElement('input');
        fontSizeInput.type = 'number';
        fontSizeInput.min = '1';
        fontSizeInput.max = '100';
        fontSizeInput.value = parseInt(getComputedStyle(document.body).fontSize, 10);
        fontSizeContainer.appendChild(fontSizeInput);

        this.container.appendChild(fontSizeContainer);

        
        const textColorContainer = document.createElement('div');
        
        const textColorLabel = document.createElement('label');
        textColorLabel.textContent = 'Цвет текста:';
        textColorContainer.appendChild(textColorLabel);
        
        const textColorInput = document.createElement('input');
        textColorInput.type = 'color';
        textColorInput.value = this.rgbToHex(getComputedStyle(document.body).color);
        textColorContainer.appendChild(textColorInput);
        
        this.container.appendChild(textColorContainer);
        
        
        const bgColorContainer = document.createElement('div');
        
        const bgColorLabel = document.createElement('label');
        bgColorLabel.textContent = 'Цвет фона:';
        bgColorContainer.appendChild(bgColorLabel);
        
        const bgColorInput = document.createElement('input');
        bgColorInput.type = 'color';
        bgColorInput.value = this.rgbToHex(getComputedStyle(document.body).backgroundColor)
        bgColorContainer.appendChild(bgColorInput);

        this.container.appendChild(bgColorContainer);
        
        fontSizeInput.addEventListener('input', () => {
            // document.querySelectorAll('*').forEach(e => e.style.fontSize = fontSizeInput.value + 'px');
            document.body.style.fontSize = fontSizeInput.value + 'px';
        });

        textColorInput.addEventListener('input', () => {
            // document.querySelectorAll('*').forEach(e => e.style.color = textColorInput.value);
            document.body.style.color = textColorInput.value;
            console.log(textColorInput.value);
        });

        bgColorInput.addEventListener('input', () => {
            // document.querySelectorAll('*').forEach(e => e.style.backgroundColor = bgColorInput.value);
            document.body.style.backgroundColor = bgColorInput.value;
        });
    }
}

export default StyleController;