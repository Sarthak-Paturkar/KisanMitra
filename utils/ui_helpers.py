import streamlit as st

def page_header(icon: str, title: str, subtitle: str):
    """Renders a styled page header with a dark green gradient banner."""
    html = f"""
    <div style="
        background: linear-gradient(135deg, #1a3c2e, #2d6a4f);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h1 style="margin: 0; font-family: Georgia, serif; color: white;">
            {icon} {title}
        </h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            {subtitle}
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def metric_card(label: str, value: str, delta: str = None, icon: str = ""):
    """Renders a styled metric card."""
    delta_html = ""
    if delta:
        color = "green" if not str(delta).startswith("-") else "red"
        delta_html = f'<div style="color: {color}; font-size: 0.9rem; font-weight: bold;">{delta}</div>'
        
    html = f"""
    <div style="
        background-color: white;
        border-left: 4px solid #2d6a4f;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    ">
        <div style="color: #666; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
            {icon} {label}
        </div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #1b4332; margin: 0.5rem 0;">
            {value}
        </div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def info_box(text: str, type: str = "info"):
    """Renders a styled info/warning/danger box."""
    colors = {
        "info": ("#e6f4ea", "#137333", "ℹ️"),
        "warn": ("#fef7e0", "#b06000", "⚠️"),
        "danger": ("#fce8e6", "#c5221f", "🚨")
    }
    bg, fg, icon = colors.get(type, colors["info"])
    
    html = f"""
    <div style="
        background-color: {bg};
        color: {fg};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid {fg};
    ">
        <strong>{icon}</strong> {text}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


