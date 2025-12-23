// scripts/charts.js
function renderStockChart(historical, forecast) {
    const trace1 = {
        x: historical.map(d => d.Date),
        y: historical.map(d => d.Close || d.Price),
        name: 'Past Data',
        type: 'scatter'
    };

    const trace2 = {
        x: forecast.map(d => d.Date),
        y: forecast.map(d => d.Price),
        name: 'Future Forecast',
        type: 'scatter',
        line: { dash: 'dot', color: 'red' }
    };

    const layout = { title: 'Stock Price Prediction' };
    Plotly.newPlot('priceChart', [trace1, trace2], layout);
}