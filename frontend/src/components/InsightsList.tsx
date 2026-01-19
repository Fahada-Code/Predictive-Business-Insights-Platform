import { Lightbulb, ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';

export function InsightsList({ insights, recommendations }: { insights: string[], recommendations: string[] }) {
    return (
        <div className="insights-grid">
            <div className="glass-panel insights-panel">
                <h3 className="panel-title"><Lightbulb className="title-icon" /> Analytical Findings</h3>
                <div className="insights-list">
                    {insights.map((insight, idx) => (
                        <motion.div
                            key={idx}
                            className="insight-item"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            dangerouslySetInnerHTML={{ __html: insight }}
                        />
                    ))}
                </div>
            </div>

            {recommendations.length > 0 && (
                <div className="glass-panel recommendations-panel">
                    <h3 className="panel-title"><ShieldAlert className="title-icon" style={{ color: '#3b82f6' }} /> Recommended Actions</h3>
                    <div className="insights-list">
                        {recommendations.map((rec, idx) => (
                            <motion.div
                                key={idx}
                                className="insight-item recommendation-item"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                dangerouslySetInnerHTML={{ __html: rec }}
                            />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
