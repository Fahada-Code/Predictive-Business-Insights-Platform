import {
    ComposedChart,
    Line,
    Scatter,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Area,
    Brush
} from 'recharts';


interface ForecastChartProps {
    data: any[];
    anomalies: any[];
}

export function ForecastChart({ data, anomalies }: ForecastChartProps) {
    // Merge anomalies into chart data
    const chartData = data.map(point => {
        const anomaly = anomalies.find(a => new Date(a.ds).getTime() === new Date(point.ds).getTime());
        return {
            ...point,
            anomalyValue: anomaly ? anomaly.y : null,
        };
    });

    return (
        <div className="glass-panel chart-panel">
            <div className="panel-header">
                <h2>Forecast & Anomaly Detection</h2>
                <div className="badges">
                    <span className="badge">Drag to Zoom</span>
                </div>
            </div>

            <div style={{ width: '100%', height: 450 }}>
                <ResponsiveContainer>
                    <ComposedChart data={chartData}>
                        <defs>
                            <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                        <XAxis
                            dataKey="ds"
                            tickFormatter={(tick) => new Date(tick).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                            stroke="#64748b"
                        />
                        <YAxis stroke="#64748b" tickFormatter={(val) => typeof val === 'number' ? val.toLocaleString(undefined, { maximumFractionDigits: 1 }) : val} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '8px', color: '#0f172a', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                            labelFormatter={(label) => new Date(label).toDateString()}
                            formatter={(value: any) => typeof value === 'number' ? [value.toFixed(2), ''] : ['', '']}
                        />
                        <Legend wrapperStyle={{ paddingTop: '20px' }} />

                        <Area
                            type="monotone"
                            dataKey="yhat_upper"
                            stroke="none"
                            fill="#3b82f6"
                            fillOpacity={0.1}
                        />

                        <Line
                            type="monotone"
                            dataKey="yhat"
                            stroke="#0ea5e9"
                            name="Forecast"
                            dot={false}
                            strokeWidth={3}
                            activeDot={{ r: 8 }}
                        />

                        <Line
                            type="monotone"
                            dataKey="yhat_upper"
                            stroke="#3b82f6"
                            name="Confidence Bounds"
                            strokeDasharray="5 5"
                            dot={false}
                            strokeWidth={1}
                        />
                        <Line
                            type="monotone"
                            dataKey="yhat_lower"
                            stroke="#3b82f6"
                            name=""
                            strokeDasharray="5 5"
                            dot={false}
                            strokeWidth={1}
                            legendType='none'
                        />

                        <Scatter
                            dataKey="anomalyValue"
                            name="Anomaly"
                            fill="#ef4444"
                            shape="circle"
                        />

                        <Brush dataKey="ds" height={30} stroke="#3b82f6" fill="#f8fafc" />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
