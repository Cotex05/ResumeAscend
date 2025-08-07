import plotly.graph_objects as go
import plotly.express as px
from typing import Dict

def create_score_chart(overall_score: int) -> go.Figure:
    """
    Create a gauge chart for overall ATS score
    
    Args:
        overall_score (int): Overall ATS compatibility score (0-100)
        
    Returns:
        go.Figure: Plotly gauge chart
    """
    
    # Determine color based on score
    if overall_score >= 80:
        color = "green"
    elif overall_score >= 60:
        color = "orange"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = overall_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ATS Compatibility Score", 'font': {'size': 24}},
        delta = {'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'lightgray'},
                {'range': [50, 80], 'color': 'gray'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        font={'color': "darkblue", 'family': "Arial"},
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    
    return fig

def create_category_breakdown(category_scores: Dict[str, int]) -> go.Figure:
    """
    Create a radar chart for category breakdown
    
    Args:
        category_scores (Dict[str, int]): Dictionary of category names and scores
        
    Returns:
        go.Figure: Plotly radar chart
    """
    
    # Prepare data for radar chart
    categories = list(category_scores.keys())
    scores = list(category_scores.values())
    
    # Clean up category names for display
    display_categories = [cat.replace('_', ' ').title() for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=display_categories,
        fill='toself',
        name='Your Score',
        line_color='#0A66C2',
        fillcolor='rgba(10, 102, 194, 0.3)'
    ))
    
    # Add reference line at 80 (good score threshold)
    fig.add_trace(go.Scatterpolar(
        r=[80] * len(categories),
        theta=display_categories,
        mode='lines',
        name='Target Score (80)',
        line=dict(color='#057642', dash='dash', width=2),
        showlegend=True
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='',
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                gridcolor='lightgray'
            )
        ),
        showlegend=True,
        height=400,
        title={
            'text': "Category Performance",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        font={'family': "Arial"},
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    
    return fig

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
                marker_color='#0A66C2',
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
                marker_color=['#E37400', '#0A66C2'],
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
            gridcolor='lightgray'
        ),
        xaxis=dict(
            title="",
            gridcolor='lightgray'
        ),
        height=300,
        font={'family': "Arial"},
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )
    
    # Add target line at 80
    fig.add_hline(
        y=80, 
        line_dash="dash", 
        line_color="#057642",
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
            marker_colors=['#057642'],
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
            'High': '#CC1016',
            'Medium': '#E37400', 
            'Low': '#00A0DC'
        }
        
        labels = list(severity_counts.keys())
        values = list(severity_counts.values())
        colors = [color_map.get(label, '#0A66C2') for label in labels]
        
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
        font={'family': "Arial"},
        paper_bgcolor="white",
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
            marker_color='#0A66C2',
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
        xaxis=dict(title="Frequency", gridcolor='lightgray'),
        yaxis=dict(title="Keywords", gridcolor='lightgray'),
        height=400,
        font={'family': "Arial"},
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )
    
    return fig
