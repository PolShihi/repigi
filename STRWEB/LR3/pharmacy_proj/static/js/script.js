import Slider from './slider.js';
import CountdownTimer from './countDownTimer.js';
import StyleController from './styleController.js';
import BirthDateModal from './birthDateModal.js';
import EmployeeTable from './tableEmployees.js';
import MedicationPagination from './medicationsPagination.js';
import BackgroundAnimation from './backgroundAnimation.js';
import TaylorSeriesChart from './taylorSeriesChart.js';

document.addEventListener('DOMContentLoaded', () => {
    const backgroundAnimation = new BackgroundAnimation(document.querySelector('.background'));

    const birthDateModal = new BirthDateModal();

    let sliderOptions = {};
    if (!!document.querySelector('#delay')) {
        sliderOptions.delay = Number(document.querySelector('#delay').getAttribute('data-value'));
    }
    const slider = new Slider(document.querySelector('.slider'), sliderOptions);

    const countDownTimer = new CountdownTimer(1000 * 60 * 60 * 1, document.querySelector('#timer'));

    const styleController = new StyleController(document.querySelector('#style-controls'));

    document.querySelector('#toggle-controls')?.addEventListener('change', (event) => {
        document.querySelector('#style-controls').style.display = event.target.checked ? 'block' : 'none';
    });

    const employeeTable = new EmployeeTable(document.querySelector('.contacts__table'));

    const medicationPagination = new MedicationPagination(document.querySelector('.shop__items'));

    const taylorSeriesChart = new TaylorSeriesChart(5);
    
    function a() {return 1;}
});