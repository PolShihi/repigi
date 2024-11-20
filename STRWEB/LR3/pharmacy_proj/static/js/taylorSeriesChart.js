class TaylorSeriesChart {
    constructor(nTerms) {
        if (!document.querySelector('#my-chart')) {
            return;
        }

        this.nTerms = nTerms;
        this.chart = null;
        this.prepareData();
        this.createChart();
        this.setupSaveButton();
    }

    seriesApproximation(x, n_terms) {
        let sum = 0;
        for (let n = 1; n <= n_terms; n++) {
            sum += (Math.pow(x, n) / n);
        }
        return -sum;
    }

    prepareData() {
        this.xValues = [];
        this.seriesValues = [];
        this.mathValues = [];
        const step = 0.01;
        for (let x = -0.99; x < 1; x += step) {
            x = parseFloat(x.toFixed(2));
            this.xValues.push(x);
            this.seriesValues.push(this.seriesApproximation(x, this.nTerms));
            this.mathValues.push(Math.log(1 - x));
        }
    }

    createChart() {
        const ctx = document.querySelector('#my-chart').getContext('2d');

        const totalDuration = 4000;
        const delayBetweenPoints = totalDuration / this.seriesValues.length;
        const animation = {
            x: {
                type: 'number',
                easing: 'easeOutCubic',
                duration: delayBetweenPoints,
                from: NaN,
                delay(ctx) {
                    if (ctx.type !== 'data' || ctx.xStarted) {
                        return 0;
                    }
                    ctx.xStarted = true;
                    return ctx.index * delayBetweenPoints;
                }
            },
            y: {
                type: 'number',
                easing: 'easeOutCubic',
                duration: delayBetweenPoints,
                from: NaN,
                delay(ctx) {
                    if (ctx.type !== 'data' || ctx.yStarted) {
                        return 0;
                    }
                    ctx.yStarted = true;
                    return ctx.index * delayBetweenPoints;
                }
            }
        };

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.xValues,
                datasets: [
                    {
                        label: `Разложение ln(1-x) (n = ${this.nTerms})`,
                        data: this.seriesValues,
                        borderColor: 'rgba(141, 153, 174, 1)',
                        backgroundColor: 'rgba(141, 153, 174, 0.2)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4
                    },
                    {
                        label: 'Функция ln(1-x)',
                        data: this.mathValues,
                        borderColor: 'rgba(239, 35, 60, 1)',
                        backgroundColor: 'rgba(239, 35, 60, 0.2)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                animation: animation,
                plugins: {
                    title: {
                        display: true,
                        text: 'Графики ln(1-x) и его разложения в ряд Тейлора',
                        font: {
                            size: 20,
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                },
                elements: {
                    point: {
                        radius: 0,
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'x',
                            font: {
                                size: 12
                            },
                            align: 'end'
                        },
                        ticks: {
                            font: {
                                size: 9
                            }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'F(x)',
                            font: {
                                size: 12
                            },
                            align: 'end'
                        },
                        ticks: {
                            font: {
                                size: 12
                            }
                        },
                        beginAtZero: false
                    }
                }
            }
        });
    }

    setupSaveButton() {
        const saveButton = document.querySelector('#save-chart');
        saveButton.addEventListener('click', () => this.saveChart());
    }

    saveChart() {
        const link = document.createElement('a');
        link.href = this.chart.toBase64Image();
        link.download = 'chart.png';
        link.click();
    }
}

export default TaylorSeriesChart;