import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import webbrowser
import os

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
    title="Enhanced Project Gantt Chart - Software Development Lifecycle",
    hover_data={"Hover_Text": True, "Start": False, "End": False, "Phase": False},
    labels={"Phase": "Project Phase"}
)

fig.update_yaxes(autorange="reversed")

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    height=600,
    width=1200,
    title={
        'text': "Enhanced Project Gantt Chart - Software Development Lifecycle",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#2C3E50'}
    },
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='white',
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#2C3E50"
    ),
    margin=dict(l=200, r=50, t=100, b=50),
    legend=dict(
        title="Project Phases",
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#CCCCCC",
        borderwidth=1
    ),
    xaxis=dict(
        rangeslider=dict(visible=True),
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
    {"date": "2023-03-11", "label": "Customer Approval", "color": "#E74C3C"},
    {"date": "2023-05-10", "label": "Project Complete", "color": "#27AE60"}
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

# ===== ADD TODAY'S DATE MARKER (if within project timeline) =====
today = datetime.now()
project_start = df['Start'].min()
project_end = df['End'].max()

if project_start <= today <= project_end:
    fig.add_vline(
        x=pd.to_datetime(today).timestamp() * 1000,
        line_dash="solid",
        line_color="#FF6B6B",
        line_width=2,
        annotation_text="Today",
        annotation_position="top",
        annotation_font_color="#FF6B6B"
    )

# ===== GENERATE STATIC IMAGE FOR PDF =====
print("Generating static image for PDF...")
try:
    fig.write_image("gantt_chart_for_pdf.png", width=1200, height=800, scale=2)
    print("✓ PNG image saved successfully!")
except Exception as e:
    print(f"Warning: Could not generate PNG (you may need to install kaleido): {e}")

# ===== CREATE TASK DETAILS TABLE HTML =====
task_details_html = """
<div class="task-details-page">
    <h2>Task Details</h2>
    <table class="task-table">
        <thead>
            <tr>
                <th>Task</th>
                <th>Phase</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Duration</th>
                <th>Progress</th>
            </tr>
        </thead>
        <tbody>
"""

for _, row in df.iterrows():
    color = phase_colors.get(row['Phase'], '#000000')
    task_details_html += f"""
            <tr>
                <td>{row['Task']}</td>
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

# ===== SAVE INTERACTIVE HTML WITH PDF DOWNLOAD AND TASK DETAILS =====
html_string = '''
<html>
<head>
    <meta charset="utf-8" />
    <title>Enhanced Project Gantt Chart</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .download-section {
            text-align: center;
            margin: 20px 0;
        }
        .download-btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #45B7D1;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 0 10px;
            cursor: pointer;
            border: none;
            font-size: 16px;
        }
        .download-btn:hover {
            background-color: #357a9a;
        }
        .task-details-page {
            background-color: white;
            padding: 30px;
            margin: 30px 0;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            page-break-before: always;
        }
        .task-details-page h2 {
            color: #2C3E50;
            margin-bottom: 20px;
            text-align: center;
        }
        .task-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .task-table th {
            background-color: #2C3E50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        .task-table td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .task-table tr:hover {
            background-color: #f5f5f5;
        }
        .phase-badge {
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }
        .progress-bar {
            position: relative;
            width: 100%;
            height: 20px;
            background-color: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background-color: #4CAF50;
            transition: width 0.3s ease;
        }
        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 12px;
            font-weight: bold;
            color: #333;
        }
        @media print {
            .download-section {
                display: none;
            }
            .task-details-page {
                page-break-before: always;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Project Gantt Chart</h1>
        <div class="download-section">
            <button class="download-btn" onclick="window.print()">📄 Print / Save as PDF</button>
            <a class="download-btn" href="gantt_chart_for_pdf.png" download="gantt_chart.png">📥 Download as Image</a>
        </div>
    </div>
    {plot_div}
    {task_details}
</body>
</html>
'''

# Write the HTML file with the interactive chart and task details
with open("gantt_chart_final.html", 'w') as f:
    f.write(html_string.replace('{plot_div}', fig.to_html(include_plotlyjs='cdn')).replace('{task_details}', task_details_html))

print("\n✓ Interactive Gantt chart saved to 'gantt_chart_final.html'")
print("\nFeatures:")
print("- Fully interactive chart (zoom, pan, hover)")
print("- Task details table (appears in PDF)")
print("- Print/Save as PDF button")
print("- Download as PNG image")
print("\nOpening in browser...")

# Open in browser
file_path = os.path.abspath("gantt_chart_final.html")
webbrowser.open(f"file://{file_path}")