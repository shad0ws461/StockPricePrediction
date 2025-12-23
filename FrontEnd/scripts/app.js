document.getElementById('forecastForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const ticker = document.getElementById('ticker').value.toUpperCase();
    const days = document.getElementById('days').value;
    const messageEl = document.getElementById('message');
    const resultsSec = document.getElementById('results');

    messageEl.style.color = "blue";
    messageEl.textContent = "Connecting to Backend...";

    try {
        // Backend API call
        const response = await fetch('http://127.0.0.1:8000/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ticker: ticker,
                days: parseInt(days)
            })
        });

        if (!response.ok) throw new Error('Backend error ya ticker galat hai.');

        const data = await response.json();

        if (data.status === "success") {
            messageEl.textContent = "";
            resultsSec.classList.remove('hidden');
            
            // Text data update karein
            document.getElementById('result-ticker').textContent = data.ticker;
            document.getElementById('prediction-horizon').textContent = days;
            
            // Forecast price dikhayein
            const forecast = data.forecast_data;
            const lastPrice = forecast[forecast.length - 1].Price;
            document.getElementById('predicted-price').textContent = lastPrice.toFixed(2);

            // Chart render karein
            renderStockChart(data.historical_data, data.forecast_data, ticker);
        }

    } catch (error) {
        console.error("Error:", error);
        messageEl.style.color = "red";
        messageEl.textContent = "Error: Backend se connection fail hua. Check karein ki Uvicorn chal raha hai.";
    }
});

function renderStockChart(historical, forecast, ticker) {
    const histTrace = {
        x: historical.map(d => d.Date),
        y: historical.map(d => d.Close || d.Price),
        name: 'Historical',
        type: 'scatter',
        mode: 'lines',
        line: { color: '#17BECF' }
    };

    const foreTrace = {
        x: forecast.map(d => d.Date),
        y: forecast.map(d => d.Price),
        name: 'Forecast',
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#FF5733', dash: 'dot' }
    };

    const layout = {
        title: `${ticker} Forecast`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price (USD)' }
    };

    Plotly.newPlot('priceChart', [histTrace, foreTrace], layout);
}