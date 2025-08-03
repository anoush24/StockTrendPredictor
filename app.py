from flask import Flask, render_template, request
from scraper import get_stock_data, scrape_financial_news
from predictor import predict_trend
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form.get('ticker', 'TSLA').upper()
        data = get_stock_data(ticker)

        if not data.empty:
            # Generate plot
            plt.style.use('ggplot')
            fig, ax = plt.subplots(figsize=(10, 5))

            # Historical data
            ax.plot(data.index, data['Close'],
                    label='Historical',
                    linewidth=2,
                    color='#1f77b4')

            # Forecast
            forecast_days = 5
            forecast = predict_trend(data, forecast_days)
            last_date = data.index[-1]
            future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, forecast_days + 1)]

            ax.plot(future_dates, forecast,
                    label='Forecast',
                    linestyle='--',
                    linewidth=2,
                    color='#ff7f0e')

            # Formatting
            ax.set_title(f'{ticker} Stock Price Prediction', fontsize=14, pad=20)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Price ($)', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save plot to buffer
            img = io.BytesIO()
            plt.savefig(img, format='png', dpi=100)
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')
            plt.close()

            # Get news and render results
            news = scrape_financial_news(ticker)
            last_price = data['Close'].iloc[-1]

            return render_template('result.html',
                                   ticker=ticker,
                                   current_price=f"{last_price:.2f}",
                                   forecast_price=f"{forecast[-1]:.2f}",
                                   trend="Upward" if forecast[-1] > last_price else "Downward",
                                   plot_url=plot_url,
                                   news=news)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)