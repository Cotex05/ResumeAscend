import plotly.graph_objects as go
from typing import Dict


PAPER = "#F3EFE7"
PAPER_DEEP = "#E8E1D5"
INK = "#1E2A27"
BRASS = "#B38B4D"
MUTED_INK = "rgba(30, 42, 39, 0.62)"


def _apply_editorial_layout(fig: go.Figure, height: int) -> go.Figure:
    """Apply the shared visual language to a Plotly figure."""
    fig.update_layout(
        height=height,
        margin=dict(l=36, r=36, t=42, b=36),
        font=dict(color=INK, family="Arial, sans-serif"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(
            bgcolor=INK,
            bordercolor=INK,
            font=dict(color=PAPER),
        ),
    )
    return fig


def create_score_chart(overall_score: int) -> go.Figure:
    """Create a restrained gauge for the overall ATS score."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=overall_score,
            domain={"x": [0.08, 0.92], "y": [0.05, 0.9]},
            title={
                "text": "ATS COMPATIBILITY",
                "font": {"size": 13, "color": MUTED_INK, "family": "Arial, sans-serif"},
            },
            number={
                "suffix": " / 100",
                "font": {"size": 44, "color": INK, "family": "Georgia, serif"},
            },
            gauge={
                "shape": "angular",
                "axis": {
                    "range": [0, 100],
                    "tickvals": [0, 20, 40, 60, 80, 100],
                    "tickfont": {"size": 10, "color": MUTED_INK},
                    "tickcolor": "rgba(30,42,39,0.18)",
                },
                "bar": {"color": BRASS, "thickness": 0.28},
                "bgcolor": PAPER_DEEP,
                "borderwidth": 0,
                "threshold": {
                    "line": {"color": INK, "width": 3},
                    "thickness": 0.7,
                    "value": 80,
                },
            },
        )
    )
    return _apply_editorial_layout(fig, 360)


def create_category_breakdown(category_scores: Dict[str, int]) -> go.Figure:
    """Create a readable horizontal score profile by category."""
    ordered_scores = sorted(category_scores.items(), key=lambda item: item[1])
    categories = [name.replace("_", " ").title() for name, _ in ordered_scores]
    scores = [score for _, score in ordered_scores]

    fig = go.Figure(
        go.Bar(
            x=scores,
            y=categories,
            orientation="h",
            marker=dict(color=BRASS, line=dict(color=INK, width=0.5)),
            text=[f"{score}" for score in scores],
            textposition="outside",
            textfont=dict(color=INK, size=12),
            hovertemplate="%{y}: %{x}/100<extra></extra>",
            width=0.48,
        )
    )
    fig.add_vline(
        x=80,
        line_width=1.5,
        line_dash="dot",
        line_color=INK,
        annotation_text="Target 80",
        annotation_position="top",
        annotation_font=dict(color=MUTED_INK, size=11),
    )
    fig.update_xaxes(
        range=[0, 106],
        showgrid=True,
        gridcolor="rgba(30,42,39,0.08)",
        zeroline=False,
        tickvals=[0, 20, 40, 60, 80, 100],
        tickfont=dict(color=MUTED_INK),
        fixedrange=True,
    )
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(color=INK, size=12),
        fixedrange=True,
    )
    fig.update_layout(showlegend=False, bargap=0.42)
    return _apply_editorial_layout(fig, 350)

def create_score_comparison(current_score: int, previous_score: int = None) -> go.Figure:
    """
    Create a comparison chart showing score improvement
    
    Args:
        current_score (int): Current ATS score
        previous_score (int, optional): Previous score for comparison
        
    Returns:
        go.Figure: Plotly bar chart
    """
    
    if previous_score is None:
        # Single score display
        fig = go.Figure(data=[
            go.Bar(
                x=['Current Score'],
                y=[current_score],
                marker_color=BRASS,
                text=[f'{current_score}%'],
                textposition='auto',
            )
        ])
        
        title_text = "Your ATS Compatibility Score"
    else:
        # Comparison display
        improvement = current_score - previous_score
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Previous Score', 'Current Score'],
                y=[previous_score, current_score],
                marker_color=[PAPER_DEEP, BRASS],
                text=[f'{previous_score}%', f'{current_score}%'],
                textposition='auto',
            )
        ])
        
        title_text = f"Score Improvement: {improvement:+d} points"
    
    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        yaxis=dict(
            range=[0, 100],
            title="Score",
            gridcolor='rgba(30,42,39,0.08)'
        ),
        xaxis=dict(
            title="",
            gridcolor='rgba(30,42,39,0.08)'
        ),
        height=300,
        font={'family': "Arial", 'color': INK},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    
    # Add target line at 80
    fig.add_hline(
        y=80, 
        line_dash="dash", 
        line_color=INK,
        annotation_text="Target Score (80)"
    )
    
    return fig

def create_issues_distribution(recommendations: list) -> go.Figure:
    """
    Create a pie chart showing distribution of issues by severity
    
    Args:
        recommendations (list): List of recommendation dictionaries
        
    Returns:
        go.Figure: Plotly pie chart
    """
    
    if not recommendations:
        # No issues found
        fig = go.Figure(data=[go.Pie(
            labels=['No Issues Found'],
            values=[1],
            marker_colors=[BRASS],
            textinfo='label',
            textposition='inside'
        )])
        
        title_text = "Issue Analysis: All Good!"
    else:
        # Count issues by severity
        severity_counts = {}
        for rec in recommendations:
            severity = rec['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Define colors for each severity
        color_map = {
            'High': INK,
            'Medium': BRASS,
            'Low': PAPER_DEEP
        }
        
        labels = list(severity_counts.keys())
        values = list(severity_counts.values())
        colors = [color_map.get(label, BRASS) for label in labels]
        
        fig = go.Figure(data=[go.Pie(
            labels=[f'{label} Priority' for label in labels],
            values=values,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='inside'
        )])
        
        title_text = f"Issues by Priority ({sum(values)} total)"
    
    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        height=300,
        font={'family': "Arial", 'color': INK},
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True
    )
    
    return fig

def create_keyword_density_chart(keyword_data: Dict[str, int]) -> go.Figure:
    """
    Create a horizontal bar chart for keyword frequency
    
    Args:
        keyword_data (Dict[str, int]): Dictionary of keywords and their frequencies
        
    Returns:
        go.Figure: Plotly horizontal bar chart
    """
    
    # Sort keywords by frequency
    sorted_keywords = sorted(keyword_data.items(), key=lambda x: x[1], reverse=True)
    keywords = [item[0] for item in sorted_keywords[:10]]  # Top 10
    frequencies = [item[1] for item in sorted_keywords[:10]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=frequencies,
            y=keywords,
            orientation='h',
            marker_color=BRASS,
            text=frequencies,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title={
            'text': "Top Keywords Found",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis=dict(title="Frequency", gridcolor='rgba(30,42,39,0.08)'),
        yaxis=dict(title="Keywords", gridcolor='rgba(30,42,39,0.08)'),
        height=400,
        font={'family': "Arial", 'color': INK},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    
    return fig
