import plotly.express as px
import pandas as pd
from datetime import datetime
import webbrowser
import os

# ===== DATA DEFINITION SECTION =====
data = [
    {"Task": "Collect Requirements", "Start": "2025-01-22", "End": "2025-02-04", "Phase": "Planning", "Progress": 85},
    {"Task": "Create Use Case Diagrams", "Start": "2025-02-11", "End": "2025-02-18", "Phase": "Design", "Progress": 75},
    {"Task": "Build Activity Diagrams", "Start": "2025-02-15", "End": "2025-03-09", "Phase": "Design", "Progress": 60},
    {"Task": "Research UI Designs", "Start": "2025-02-27", "End": "2025-03-07", "Phase": "Design", "Progress": 45},
    {"Task": "Build Class Diagram", "Start": "2025-03-01", "End": "2025-03-09", "Phase": "Design", "Progress": 30},
    {"Task": "Get Customer Approval", "Start": "2025-03-10", "End": "2025-03-11", "Phase": "Approval", "Progress": 0},
    {"Task": "Build Interface", "Start": "2025-03-12", "End": "2025-03-24", "Phase": "Development", "Progress": 0},
    {"Task": "Link DB to Interface", "Start": "2025-03-24", "End": "2025-04-03", "Phase": "Development", "Progress": 0},
    {"Task": "Build Business Logic", "Start": "2025-04-05", "End": "2025-04-27", "Phase": "Development", "Progress": 0},
    {"Task": "Test System", "Start": "2025-04-27", "End": "2025-05-07", "Phase": "Testing", "Progress": 0},
    {"Task": "Deliver System", "Start": "2025-05-08", "End": "2025-05-09", "Phase": "Deployment", "Progress": 0},
    {"Task": "Sign-off Meeting", "Start": "2025-05-09", "End": "2025-05-10", "Phase": "Deployment", "Progress": 0},
]

# ===== DATA PREPROCESSING SECTION =====
df = pd.DataFrame(data)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Duration'] = (df['End'] - df['Start']).dt.days + 1

df['Hover_Text'] = df.apply(lambda row:
                            f"<b>{row['Task']}</b><br>" +
                            f"Phase: {row['Phase']}<br>" +
                            f"Start: {row['Start'].strftime('%B %d, %Y')}<br>" +
                            f"End: {row['End'].strftime('%B %d, %Y')}<br>" +
                            f"Duration: {row['Duration']} days<br>" +
                            f"Progress: {row['Progress']}%",
                            axis=1
                            )

# ===== COLOR SCHEME DEFINITION =====
phase_colors = {
    "Planning": "#FF6B6B",
    "Design": "#4ECDC4",
    "Approval": "#FFE66D",
    "Development": "#45B7D1",
    "Testing": "#96CEB4",
    "Deployment": "#9B59B6"
}

df['Color'] = df['Phase'].map(phase_colors)

# ===== GANTT CHART CREATION =====
fig = px.timeline(
    df,
    x_start="Start",
    x_end="End",
    y="Task",
    color="Phase",
    color_discrete_map=phase_colors,
    title="Project Gantt Chart - Software Development Lifecycle",
    hover_data={"Hover_Text": True, "Start": False, "End": False, "Phase": False},
    labels={"Phase": "Project Phase"}
)

fig.update_yaxes(autorange="reversed")

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>",
    textposition="inside",
    insidetextanchor="middle"
)

# ===== LAYOUT FOR BETTER PDF EXPORT =====
fig.update_layout(
    height=800,  # Increased height for PDF
    width=1400,  # Increased width to prevent cutoff
    title={
        'text': "Project Gantt Chart - Software Development Lifecycle",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#2C3E50'}
    },
    plot_bgcolor='white',  # White background for print
    paper_bgcolor='white',
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#2C3E50"
    ),
    margin=dict(l=200, r=150, t=100, b=100),  # Increased margins
    legend=dict(
        title="Project Phases",
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="white",
        bordercolor="#333333",
        borderwidth=1
    ),
    xaxis=dict(
        rangeslider=dict(
            visible=True,
            thickness=0.04
        ),
        type="date",
        tickformat="%b %d\n%Y",
        showgrid=True,
        gridcolor='#E0E0E0'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        tickfont=dict(size=11)
    )
)

# ===== ADD MILESTONE MARKERS =====
milestones = [
    {"date": "2025-03-11", "label": "Customer Approval", "color": "#E74C3C"},
    {"date": "2025-05-10", "label": "Project Complete", "color": "#27AE60"}
]

for milestone in milestones:
    fig.add_vline(
        x=pd.to_datetime(milestone["date"]).timestamp() * 1000,
        line_dash="dash",
        line_color=milestone["color"],
        annotation_text=milestone["label"],
        annotation_position="top",
        annotation_font_color=milestone["color"],
        annotation_font_size=10
    )

# ===== GENERATE STATIC IMAGE FOR PDF =====
print("Generating static image for PDF...")
try:
    fig.write_image("gantt_chart_for_pdf.png", width=1400, height=800, scale=2)
    print("✓ PNG image saved successfully!")
except Exception as e:
    print(f"Warning: Could not generate PNG (you may need to install kaleido): {e}")

# ===== CREATE TASK DETAILS TABLE HTML =====
task_details_html = """
<div class="task-details-page">
    <h2 class="section-title">Task Details</h2>
    <p class="section-subtitle">Progress values are theoretical projections</p>
    <table class="task-table">
        <thead>
            <tr>
                <th>Task</th>
                <th>Phase</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Duration</th>
                <th>Progress (Projected)</th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in df.iterrows():
    color = phase_colors.get(row['Phase'], '#000000')
    task_details_html += f"""
            <tr>
                <td class="task-name">{row['Task']}</td>
                <td><span class="phase-badge" style="background-color: {color};">{row['Phase']}</span></td>
                <td>{row['Start'].strftime('%B %d, %Y')}</td>
                <td>{row['End'].strftime('%B %d, %Y')}</td>
                <td>{row['Duration']} days</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {row['Progress']}%"></div>
                        <span class="progress-text">{row['Progress']}%</span>
                    </div>
                </td>
            </tr>
"""

task_details_html += """
        </tbody>
    </table>
</div>
"""

# ===== SAVE INTERACTIVE HTML WITH PRINT-OPTIMIZED CSS =====
html_string = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Project Gantt Chart | Modern Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Screen styles */
        @media screen {
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #0A0E27 0%, #151932 50%, #0A0E27 100%);
                color: #E0E6ED;
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }
            
            /* Animated background grid */
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    repeating-linear-gradient(0deg, transparent, transparent 70px, rgba(0, 212, 255, 0.03) 70px, rgba(0, 212, 255, 0.03) 71px),
                    repeating-linear-gradient(90deg, transparent, transparent 70px, rgba(0, 212, 255, 0.03) 70px, rgba(0, 212, 255, 0.03) 71px);
                pointer-events: none;
                z-index: 1;
            }
            
            /* Glow effects */
            .glow {
                position: fixed;
                width: 500px;
                height: 500px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
                z-index: 1;
                animation: floatGlow 20s infinite ease-in-out;
            }
            
            @keyframes floatGlow {
                0%, 100% { transform: translate(0, 0) scale(1); }
                33% { transform: translate(30px, -30px) scale(1.1); }
                66% { transform: translate(-20px, 20px) scale(0.9); }
            }
            
            h1 {
                font-family: 'JetBrains Mono', monospace;
                font-size: 3.5rem;
                font-weight: 700;
                letter-spacing: -2px;
                background: linear-gradient(45deg, #00D4FF, #00FFF0, #9D4EDD);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.5));
            }
            
            .glass-btn {
                position: relative;
                padding: 15px 40px;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 50px;
                color: #E0E6ED;
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 1px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
            }
            
            .glass-btn.primary {
                border-color: rgba(0, 212, 255, 0.5);
                background: rgba(0, 212, 255, 0.1);
            }
            
            .chart-wrapper {
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                margin: 30px 0;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            }
            
            .task-details-page {
                background: rgba(255, 255, 255, 0.02);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 40px;
                margin: 40px 0;
            }
            
            .phase-badge {
                color: #FFFFFF;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            }
            
            .progress-bar {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .progress-fill {
                background: linear-gradient(90deg, #00D4FF, #45B7D1);
                box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
            }
        }
        
        /* PRINT STYLES - CRITICAL FOR PDF EXPORT */
        @media print {
            @page {
                size: A4 landscape;
                margin: 10mm;
            }
            
            body {
                font-family: Arial, sans-serif !important;
                background: white !important;
                color: black !important;
                margin: 0;
                padding: 0;
            }
            
            /* Hide screen-only elements */
            body::before,
            .glow,
            .download-section {
                display: none !important;
            }
            
            /* Container adjustments */
            .container {
                max-width: 100% !important;
                padding: 0 !important;
            }
            
            /* Header styles for print */
            .header {
                page-break-after: avoid;
                margin-bottom: 20px !important;
            }
            
            h1 {
                font-family: Arial, sans-serif !important;
                font-size: 28pt !important;
                color: #2C3E50 !important;
                background: none !important;
                -webkit-text-fill-color: #2C3E50 !important;
                filter: none !important;
                text-align: center;
                margin-bottom: 10px;
            }
            
            .subtitle {
                font-size: 14pt !important;
                color: #555 !important;
                text-align: center;
            }
            
            /* Chart wrapper for print */
            .chart-wrapper {
                background: white !important;
                border: 1px solid #ddd !important;
                border-radius: 0 !important;
                padding: 10px !important;
                box-shadow: none !important;
                page-break-inside: avoid;
                margin: 20px 0 !important;
            }
            
            /* Plotly chart specific */
            .plotly-graph-div {
                width: 100% !important;
                height: auto !important;
                background: white !important;
            }
            
            /* Force white background on plotly elements */
            .plotly .bg {
                fill: white !important;
            }
            
            .js-plotly-plot .plotly {
                background: white !important;
            }
            
            /* Hide range slider in print */
            .rangeslider-container {
                display: none !important;
            }
            
            /* Task details page */
            .task-details-page {
                background: white !important;
                border: none !important;
                padding: 20px 0 !important;
                page-break-before: always;
                margin-top: 0 !important;
            }
            
            
            .section-title {
                font-size: 20pt !important;
                color: #2C3E50 !important;
                margin-bottom: 10px !important;
                text-align: center;
            }
            
            .section-subtitle {
                font-size: 12pt !important;
                color: #666 !important;
                text-align: center;
                margin-bottom: 20px;
            }
            
            /* Table styles for print */
            .task-table {
                width: 100% !important;
                border-collapse: collapse !important;
                font-size: 10pt !important;
            }
            
            .task-table th {
                background-color: #f5f5f5 !important;
                color: #333 !important;
                padding: 8px !important;
                border: 1px solid #ddd !important;
                font-weight: bold !important;
                text-transform: uppercase;
                font-size: 9pt !important;
            }
            
            .task-table td {
                padding: 6px !important;
                border: 1px solid #ddd !important;
                color: #333 !important;
                background: white !important;
            }
            
            .task-table tr:nth-child(even) td {
                background-color: #fafafa !important;
            }
            
            /* Force white background for table rows */
            .task-table tbody tr {
                background: white !important;
            }
            
            .task-name {
                font-weight: bold !important;
                color: #2C3E50 !important;
            }
            
            /* Phase badges for print */
            .phase-badge {
                display: inline-block !important;
                padding: 4px 12px !important;
                border-radius: 12px !important;
                font-size: 9pt !important;
                font-weight: bold !important;
                color: white !important;
                text-shadow: none !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
            }
            
            /* Progress bars for print */
            .progress-bar {
                position: relative !important;
                width: 100% !important;
                height: 20px !important;
                background: #f0f0f0 !important;
                border: 1px solid #ccc !important;
                border-radius: 10px !important;
                overflow: hidden !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
            }
            
            .progress-fill {
                height: 100% !important;
                background: #4CAF50 !important;
                border-radius: 10px !important;
                print-color-adjust: exact !important;
                -webkit-print-color-adjust: exact !important;
            }
            
            .progress-text {
                position: absolute !important;
                top: 50% !important;
                left: 50% !important;
                transform: translate(-50%, -50%) !important;
                font-size: 9pt !important;
                font-weight: bold !important;
                color: #333 !important;
                text-shadow: none !important;
                z-index: 1;
            }
        }
        
        /* Common styles */
        .container {
            position: relative;
            z-index: 2;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 50px;
            position: relative;
        }
        
        .subtitle {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            color: #64748B;
            margin-top: 10px;
            letter-spacing: 4px;
            text-transform: uppercase;
        }
        
        .download-section {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 40px 0;
            flex-wrap: wrap;
        }
        
        .section-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            text-align: center;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00D4FF, #9D4EDD);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .section-subtitle {
            text-align: center;
            color: #64748B;
            font-style: italic;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .task-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
        }
        
        .task-table th {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748B;
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .task-table tr {
            background: rgba(255, 255, 255, 0.02);
            transition: all 0.3s ease;
        }
        
        .task-table tbody tr:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(5px);
        }
        
        .task-table td {
            padding: 15px;
            color: #E0E6ED;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .task-name {
            font-weight: 600;
            color: #00D4FF;
        }
        
        .phase-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #FFFFFF;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 0, 0, 0.2);
        }
        
        .progress-bar {
            position: relative;
            width: 100%;
            height: 28px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00D4FF, #45B7D1);
            border-radius: 14px;
            transition: width 0.6s ease;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
            position: relative;
        }
        
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 12px;
            font-weight: 700;
            color: #FFFFFF;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
            z-index: 1;
        }
    </style>
</head>
<body>
    <div class="glow" style="top: -250px; left: -250px;"></div>
    <div class="glow" style="background: radial-gradient(circle, rgba(157, 78, 221, 0.1) 0%, transparent 70%); right: -250px; top: 60%;"></div>
    
    <div class="container">
        <div class="header">
            <h1>PROJECT GANTT CHART</h1>
            <p class="subtitle">Software Development Lifecycle</p>
        </div>
        
        <div class="download-section">
            <button class="glass-btn primary" onclick="window.print()">Export PDF</button>
        </div>
        
        <div class="chart-wrapper">
            {plot_div}
        </div>
        
        {task_details}
    </div>
</body>
</html>
'''

# Write the HTML file
with open("gantt_chart_final.html", 'w') as f:
    f.write(html_string.replace('{plot_div}', fig.to_html(include_plotlyjs='cdn')).replace('{task_details}', task_details_html))

print("\n✓ Gantt chart with fixed PDF export saved to 'gantt_chart_final.html'")
print("\nFeatures:")
print("- Optimized for PDF export with print-specific CSS")
print("- Full-width chart display (no cutoff)")
print("- High contrast colors for printing")
print("- Clear phase badges and progress bars")
print("\nOpening in browser...")

# Open in browser
file_path = os.path.abspath("gantt_chart_final.html")
webbrowser.open(f"file://{file_path}")