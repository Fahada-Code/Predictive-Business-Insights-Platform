from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import pandas as pd
from typing import Dict, List, Any

def generate_pdf_report(
    forecast_df: pd.DataFrame,
    metrics: Dict[str, float],
    insights_data: Dict[str, List[str]], # Changed from insights: List[str]
    anomalies: pd.DataFrame
) -> io.BytesIO:
    """
    Generates a professional executive report for business insights.
    Returns: BytesIO object containing the PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom Styles
    styles.add(ParagraphStyle(name='ExecutiveSub', parent=styles['Normal'], fontSize=10, textColor=colors.grey))

    # Title
    story.append(Paragraph("Executive Business Analytics Report", styles['Title']))
    story.append(Paragraph("Data-driven forecasts and performance insights", styles['ExecutiveSub']))
    story.append(Spacer(1, 18))

    # 1. Performance Overview (Metrics)
    story.append(Paragraph("Model Performance Overview", styles['Heading2']))
    story.append(Spacer(1, 6))
    
    # Confidence metrics mapping
    confidence = (100 - metrics.get("MAPE", 0))
    metric_data = [
        ["Core Metric", "Analysis Value", "Status"],
        ["Model Confidence", f"{confidence:.1f}%", "Optimal" if confidence > 85 else "Review Required"],
        ["Relative Error (MAPE)", f"{metrics.get('MAPE', 0):.1f}%", "Acceptable" if metrics.get('MAPE', 0) < 15 else "Variable"],
        ["Root Mean Sq Error", str(metrics.get("RMSE", 0)), "N/A"]
    ]
        
    t = Table(metric_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#475569")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 24))

    # 2. Key Insights & Recommended Actions
    story.append(Paragraph("Analytical Findings", styles['Heading2']))
    story.append(Spacer(1, 8))
    
    insights = insights_data.get("insights", [])
    recommendations = insights_data.get("recommendations", [])
    
    for insight in insights:
        # Paragraph handles <b> and <i> tags naturally
        text = insight.replace("📊", "").replace("🚀", "").replace("⚠️", "").replace("🛡️", "").replace("✅", "").replace("🔍", "")
        story.append(Paragraph(f"<b>[FINDING]</b> {text}", styles['Normal']))
        story.append(Spacer(1, 6))

    if recommendations:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Recommended Strategic Actions", styles['Heading3']))
        story.append(Spacer(1, 6))
        for rec in recommendations:
            story.append(Paragraph(f"<font color='blue'>[ACTION]</font> {rec}", styles['Normal']))
            story.append(Spacer(1, 4))
            
    story.append(Spacer(1, 24))

    # 3. Anomaly Intelligence
    if not anomalies.empty:
        # Group by severity
        high = len(anomalies[anomalies['severity_level'] == 'High'])
        med = len(anomalies[anomalies['severity_level'] == 'Medium'])
        low = len(anomalies[anomalies['severity_level'] == 'Low'])
        
        story.append(Paragraph(f"Anomaly Detection Summary", styles['Heading2']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"Detected <b>{len(anomalies)}</b> total anomalies: {high} High, {med} Medium, {low} Low.", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Table of top critical anomalies
        anomaly_data = [["Priority", "Date", "Actual", "Forecast", "Variance %"]]
        top_anomalies = anomalies.sort_values(by='severity', ascending=False).head(10) # Top 10
        
        for _, row in top_anomalies.iterrows():
            date_str = pd.to_datetime(row['ds']).strftime('%Y-%m-%d')
            var_pct = (row['severity'] / row['yhat']) * 100
            anomaly_data.append([
                row['severity_level'],
                date_str,
                f"{row['y']:.1f}",
                f"{row['yhat']:.1f}",
                f"{var_pct:.1f}%"
            ])
            
        at = Table(anomaly_data, colWidths=[1.2*inch, 1.2*inch, 1.0*inch, 1.0*inch, 1.2*inch])
        at.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#ef4444")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(at)
    else:
        story.append(Paragraph("No statistically significant anomalies detected in this cycle.", styles['Normal']))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
