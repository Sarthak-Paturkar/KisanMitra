import plotly.graph_objects as go
import pandas as pd
import numpy as np

def make_price_chart(dates, prices, pred_dates=None, pred_prices=None, lower=None, upper=None, crop_name="Crop"):
    """
    Creates a smoothed spline chart for historical and predicted prices.
    Uses only Plotly (no matplotlib).
    """
    fig = go.Figure()

    # Historical Data
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name='Historical Price',
        line=dict(shape='spline', smoothing=1.3, color='#2d6a4f', width=2),
        fill='tozeroy',
        fillcolor='rgba(45, 106, 79, 0.1)'
    ))

    # Prediction Data
    if pred_dates is not None and pred_prices is not None:
        # Confidence Band
        if lower is not None and upper is not None:
            fig.add_trace(go.Scatter(
                x=list(pred_dates) + list(pred_dates)[::-1],
                y=list(upper) + list(lower)[::-1],
                fill='toself',
                fillcolor='rgba(244, 162, 97, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name='Confidence Interval'
            ))

        # Prediction Line
        fig.add_trace(go.Scatter(
            x=pred_dates,
            y=pred_prices,
            mode='lines',
            name='Predicted Price',
            line=dict(shape='spline', smoothing=1.3, color='#f4a261', width=2, dash='dash')
        ))

    fig.update_layout(
        title=dict(text=f"{crop_name} Price Trend", font=dict(family="Georgia, serif", size=20, color="#1b4332")),
        plot_bgcolor="#f5f0e8",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        xaxis=dict(title="", showgrid=False, zeroline=False),
        yaxis=dict(title="₹ / Quintal", showgrid=True, gridcolor='rgba(0,0,0,0.05)', zeroline=False),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig
