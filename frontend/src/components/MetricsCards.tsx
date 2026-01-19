import { Activity, TrendingUp, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

interface Metrics {
    MAE: number;
    RMSE: number;
    MAPE: number;
}

export function MetricsCards({ metrics }: { metrics: Metrics }) {
    const confidence = (100 - metrics.MAPE).toFixed(1);
    const confidenceScore = parseFloat(confidence);

    const cards = [
        {
            label: "Model Confidence",
            value: `${confidence}%`,
            caption: confidenceScore > 85 ? "Optimal predictive reliability" : "Review data for variance",
            icon: <TrendingUp size={24} color="#0ea5e9" />,
            color: confidenceScore > 85 ? "var(--accent-primary)" : "#f59e0b"
        },
        {
            label: "Forecast Error (MAPE)",
            value: `${metrics.MAPE.toFixed(1)}%`,
            caption: metrics.MAPE < 15 ? "Low relative variance" : "High historical noise",
            icon: <Activity size={24} color="#2563eb" />
        },
        {
            label: "RMSE Intensity",
            value: metrics.RMSE.toFixed(2),
            caption: "Absolute deviation magnitude",
            icon: <AlertTriangle size={24} color="#0284c7" />
        },
    ];

    return (
        <div className="metrics-grid">
            {cards.map((card, idx) => (
                <motion.div
                    key={idx}
                    className="glass-panel metric-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                >
                    <div className="metric-header">
                        <span>{card.label}</span>
                        {card.icon}
                    </div>
                    <div className="metric-value" style={{ color: card.color }}>{card.value}</div>
                    <div className="metric-caption">{card.caption}</div>
                </motion.div>
            ))}
        </div>
    );
}
