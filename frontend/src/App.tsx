import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

// Define types for forecast data
interface ForecastDataPoint {
  ds: string;
  yhat: number;
  yhat_lower: number;
  yhat_upper: number;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [days, setDays] = useState<number>(30);
  const [seasonalityMode, setSeasonalityMode] = useState<string>('additive');
  const [forecastData, setForecastData] = useState<ForecastDataPoint[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload a CSV file.");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`http://127.0.0.1:8000/forecast?days=${days}&seasonality_mode=${seasonalityMode}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setForecastData(response.data.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "An error occurred fetching the forecast.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Predictive Business Insights Dashboard</h1>

      <div className="controls">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Upload CSV Data:</label>
            <input type="file" accept=".csv,.txt" onChange={handleFileChange} />
          </div>

          <div className="form-group">
            <label>Forecast Days:</label>
            <input
              type="number"
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value))}
              min="1"
              max="365"
            />
          </div>

          <div className="form-group">
            <label>Seasonality Mode:</label>
            <select value={seasonalityMode} onChange={(e) => setSeasonalityMode(e.target.value)}>
              <option value="additive">Additive</option>
              <option value="multiplicative">Multiplicative</option>
            </select>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Generating Forecast...' : 'Generate Forecast'}
          </button>
        </form>
        {error && <p className="error">{error}</p>}
      </div>

      {forecastData.length > 0 && (
        <div className="chart-container">
          <h2>Forecast Results</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ds" tickFormatter={(tick) => new Date(tick).toLocaleDateString()} />
              <YAxis />
              <Tooltip labelFormatter={(label) => new Date(label).toLocaleDateString()} />
              <Legend />
              <Line type="monotone" dataKey="yhat" stroke="#8884d8" name="Broadcast" dot={false} />
              <Line type="monotone" dataKey="yhat_upper" stroke="#82ca9d" name="Upper Confidence" strokeDasharray="5 5" dot={false} />
              <Line type="monotone" dataKey="yhat_lower" stroke="#82ca9d" name="Lower Confidence" strokeDasharray="5 5" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default App;
