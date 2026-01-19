import { Activity, TrendingUp, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

interface Metrics {
    MAE: number;
    RMSE: number;
    MAPE: number;
}

export function MetricsCards({ metrics }: { metrics: Metrics }) {
    const confidence = (100 - metrics.MAPE).toFixed(1);

    const cards = [
        { label: "Model Confidence", value: `${confidence}%`, icon: <TrendingUp size={24} color="#0ea5e9" /> },
        { label: "Review Error (MAPE)", value: `${metrics.MAPE.toFixed(1)}%`, icon: <Activity size={24} color="#2563eb" /> },
        { label: "Root Mean Sq Error", value: metrics.RMSE.toFixed(2), icon: <AlertTriangle size={24} color="#0284c7" /> },
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
                    <div className="metric-value">{card.value}</div>
                </motion.div>
            ))}
        </div>
    );
}
