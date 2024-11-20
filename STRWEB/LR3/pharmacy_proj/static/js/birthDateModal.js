class BirthDateModal {
    constructor() {
        const hasPassedCheck = sessionStorage.getItem('ageCheckPassed');
        if (!document.querySelector('.modal') || hasPassedCheck || document.querySelector('#user-is-authenticated')) {
            return;
        }

        this.modal = document.querySelector('.modal');
        this.modalBirthDate = this.modal.querySelector('.modal-birth-date');
        this.birthDateInput = this.modal.querySelector('#birth-date');
        this.submitButton = this.modal.querySelector('#submit-birth-date');
        this.resultModal = this.modal.querySelector('.modal-birth-date-end');
        this.closeEndModal = this.modal.querySelector('.modal-birth-date-end__close');
        this.resultText = this.modal.querySelector('.modal-birth-date-end__text');

        this.init();
    }

    init() {
        this.openModal();
        this.submitButton.addEventListener('click', () => this.checkAge());;
        this.closeEndModal.addEventListener('click', () => this.closeModal());;
    }

    openModal() {
        this.modal.style.display = 'block';
        this.modalBirthDate.style.display = 'block';
    }

    closeModal() {
        this.modal.style.display = 'none';
    }

    checkAge() {
        const birthDateInput = this.birthDateInput.value;

        if (!birthDateInput) {
            alert('Please, enter your birth date.');
            return;
        }

        const birthDate = new Date(birthDateInput);
        const today = new Date();
        const age = today.getFullYear() - birthDate.getFullYear();
        const monthDifference = today.getMonth() - birthDate.getMonth();

        const isBirthdayPassed = monthDifference > 0 || (monthDifference === 0 && today.getDate() >= birthDate.getDate());
        const finalAge = isBirthdayPassed ? age : age - 1;

        const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const dayOfWeek = daysOfWeek[birthDate.getDay()];

        let resultMessage;
        if (finalAge >= 18) {
            resultMessage = `You are an adult. Your birth day of the week is: ${dayOfWeek}.`;
            sessionStorage.setItem('ageCheckPassed', 'true');
        } else {
            resultMessage = `You are a minor. You need parental permission to use this site.`;
        }

        this.resultText.textContent = resultMessage;
        this.modalBirthDate.style.display = 'none';
        this.resultModal.style.display = 'block';
    }
}

export default BirthDateModal;