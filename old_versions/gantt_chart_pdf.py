import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import plotly.io as pio

# ===== DATA DEFINITION SECTION =====
data = [
    {"Task": "Collect Requirements", "Start": "2023-01-22", "End": "2023-02-04", "Phase": "Planning", "Progress": 100},
    {"Task": "Create Use Case Diagrams", "Start": "2023-02-11", "End": "2023-02-18", "Phase": "Design", "Progress": 100},
    {"Task": "Build Activity Diagrams", "Start": "2023-02-15", "End": "2023-03-09", "Phase": "Design", "Progress": 100},
    {"Task": "Research UI Designs", "Start": "2023-02-27", "End": "2023-03-07", "Phase": "Design", "Progress": 100},
    {"Task": "Build Class Diagram", "Start": "2023-03-01", "End": "2023-03-09", "Phase": "Design", "Progress": 100},
    {"Task": "Get Customer Approval", "Start": "2023-03-10", "End": "2023-03-11", "Phase": "Approval", "Progress": 100},
    {"Task": "Build Interface", "Start": "2023-03-12", "End": "2023-03-24", "Phase": "Development", "Progress": 100},
    {"Task": "Link DB to Interface", "Start": "2023-03-24", "End": "2023-04-03", "Phase": "Development", "Progress": 100},
    {"Task": "Build Business Logic", "Start": "2023-04-05", "End": "2023-04-27", "Phase": "Development", "Progress": 100},
    {"Task": "Test System", "Start": "2023-04-27", "End": "2023-05-07", "Phase": "Testing", "Progress": 100},
    {"Task": "Deliver System", "Start": "2023-05-08", "End": "2023-05-09", "Phase": "Deployment", "Progress": 100},
    {"Task": "Sign-off Meeting", "Start": "2023-05-09", "End": "2023-05-10", "Phase": "Deployment", "Progress": 100},
]

# ===== DATA PREPROCESSING SECTION =====
df = pd.DataFrame(data)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Duration'] = (df['End'] - df['Start']).dt.days + 1

# ===== COLOR SCHEME DEFINITION =====
phase_colors = {
    "Planning": "#FF6B6B",
    "Design": "#4ECDC4", 
    "Approval": "#FFE66D",
    "Development": "#45B7D1",
    "Testing": "#96CEB4",
    "Deployment": "#9B59B6"
}

# ===== CREATE GANTT CHART FIGURE =====
fig = go.Figure()

# Group tasks by phase for better organization
phases = df['Phase'].unique()

# Add traces for each phase
for phase in phases:
    phase_df = df[df['Phase'] == phase]
    
    # Add bars for each task in the phase
    for _, task in phase_df.iterrows():
        fig.add_trace(go.Bar(
            name=task['Task'],
            x=[task['Duration']],
            y=[task['Task']],
            orientation='h',
            base=task['Start'],
            marker=dict(
                color=phase_colors[phase],
                line=dict(color='rgba(0,0,0,0.3)', width=1)
            ),
            text=f"{task['Task']}<br>Duration: {task['Duration']} days<br>Progress: {task['Progress']}%",
            textposition='inside',
            hovertemplate=(
                f"<b>{task['Task']}</b><br>"
                f"Phase: {phase}<br>"
                f"Start: {task['Start'].strftime('%B %d, %Y')}<br>"
                f"End: {task['End'].strftime('%B %d, %Y')}<br>"
                f"Duration: {task['Duration']} days<br>"
                f"Progress: {task['Progress']}%<extra></extra>"
            ),
            showlegend=False
        ))

# Add legend entries for phases
for phase, color in phase_colors.items():
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=10, color=color),
        name=phase,
        showlegend=True
    ))

# ===== LAYOUT CONFIGURATION =====
fig.update_layout(
    title={
        'text': "Project Gantt Chart - Software Development Lifecycle",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#2C3E50'}
    },
    xaxis=dict(
        title="Timeline",
        type='date',
        tickformat='%b %d\n%Y',
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False
    ),
    yaxis=dict(
        title="Tasks",
        autorange="reversed",
        showgrid=True,
        gridcolor='#E0E0E0',
        tickfont=dict(size=10)
    ),
    height=800,
    width=1200,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial, sans-serif",
        size=11,
        color="#2C3E50"
    ),
    margin=dict(l=200, r=150, t=100, b=50),
    legend=dict(
        title="Project Phases",
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#CCCCCC",
        borderwidth=1
    ),
    barmode='overlay'
)

# ===== ADD MILESTONE MARKERS =====
milestones = [
    {"date": "2023-03-11", "label": "Customer Approval", "color": "#E74C3C"},
    {"date": "2023-05-10", "label": "Project Complete", "color": "#27AE60"}
]

for milestone in milestones:
    fig.add_vline(
        x=pd.to_datetime(milestone["date"]).timestamp() * 1000,
        line_dash="dash",
        line_color=milestone["color"],
        line_width=2,
        annotation_text=milestone["label"],
        annotation_position="top",
        annotation_font_color=milestone["color"],
        annotation_font_size=10
    )

# ===== EXPORT OPTIONS =====
# 1. Save as static HTML (no JavaScript dependencies)
print("Generating static HTML...")
fig.write_html(
    "gantt_chart_static.html",
    config={'displayModeBar': False, 'staticPlot': True},
    include_plotlyjs='cdn'
)

# 2. Save as high-resolution PNG image
print("Generating PNG image...")
try:
    fig.write_image("gantt_chart.png", width=1200, height=800, scale=2)
    print("PNG saved successfully!")
except Exception as e:
    print(f"Error saving PNG: {e}")
    print("You may need to install kaleido: pip install kaleido")

# 3. Save as PDF directly
print("Generating PDF...")
try:
    fig.write_image("gantt_chart_direct.pdf", width=1200, height=800, scale=2)
    print("PDF saved successfully!")
except Exception as e:
    print(f"Error saving PDF: {e}")
    print("You may need to install kaleido: pip install kaleido")

# 4. Create a PDF-optimized HTML with inline CSS
print("Generating PDF-optimized HTML...")
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Gantt Chart - PDF Version</title>
    <style>
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
            }}
            .chart-container {{
                width: 100%;
                height: auto;
                page-break-inside: avoid;
            }}
        }}
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: white;
        }}
        h1 {{
            text-align: center;
            color: #2C3E50;
        }}
        .info {{
            margin: 20px 0;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>Project Gantt Chart - Software Development Lifecycle</h1>
    <div class="info">
        <p><strong>Project Duration:</strong> January 22, 2023 - May 10, 2023</p>
        <p><strong>Total Tasks:</strong> 12</p>
        <p><strong>Key Milestones:</strong> Customer Approval (March 11), Project Complete (May 10)</p>
    </div>
    <div class="chart-container">
        {chart}
    </div>
</body>
</html>
"""

# Generate HTML with the chart embedded
chart_html = fig.to_html(
    include_plotlyjs='cdn',
    config={'displayModeBar': False, 'staticPlot': True, 'responsive': False},
    div_id="gantt-chart"
)

# Remove the full HTML structure from chart_html to get just the div
import re
chart_div = re.search(r'<div.*?</div>', chart_html, re.DOTALL).group()

final_html = html_template.format(chart=chart_div)

with open("gantt_chart_pdf_ready.html", "w") as f:
    f.write(final_html)

print("\nAll files generated successfully!")
print("\nTo convert to PDF:")
print("1. Open 'gantt_chart_pdf_ready.html' in your browser")
print("2. Press Ctrl+P (or Cmd+P on Mac)")
print("3. Save as PDF")
print("\nAlternatively, if you have wkhtmltopdf installed:")
print("wkhtmltopdf gantt_chart_pdf_ready.html gantt_chart_final.pdf")