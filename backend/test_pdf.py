import pandas as pd
from app.utils.reporting import generate_pdf_report
import os

def test_pdf_generation():
    # Mock data
    forecast_df = pd.DataFrame({
        'ds': pd.date_range(start='2023-01-01', periods=10),
        'yhat': range(10),
        'yhat_lower': range(10),
        'yhat_upper': range(10)
    })
    metrics = {'MAPE': 10.5, 'RMSE': 5.2}
    insights = ["Test insight 1", "Test insight 2"]
    anomalies = pd.DataFrame({
        'ds': ['2023-01-05'],
        'y': [100],
        'yhat': [50],
        'severity': [50]
    })
    
    print("Generating PDF...")
    try:
        buffer = generate_pdf_report(forecast_df, metrics, insights, anomalies)
        # Attempt to write to file to check it's valid
        with open("test_report.pdf", "wb") as f:
            f.write(buffer.getvalue())
        print("PDF generated successfully: test_report.pdf")
        os.remove("test_report.pdf")
    except Exception as e:
        print(f"FAILED to generate PDF: {e}")
        exit(1)

if __name__ == "__main__":
    test_pdf_generation()
