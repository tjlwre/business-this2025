"""
Modern UI Components for BusinessThis
Reusable components with consistent styling and behavior
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class UIComponents:
    """Collection of modern UI components"""
    
    @staticmethod
    def metric_card(title, value, icon, subtitle=None, color="primary", trend=None):
        """Create a modern metric card"""
        color_map = {
            "primary": "var(--primary-600)",
            "success": "var(--success-600)", 
            "warning": "var(--warning-600)",
            "error": "var(--error-600)",
            "info": "var(--neutral-600)"
        }
        
        trend_icon = ""
        trend_color = "var(--neutral-500)"
        if trend:
            if trend > 0:
                trend_icon = "fas fa-arrow-up"
                trend_color = "var(--success-600)"
            elif trend < 0:
                trend_icon = "fas fa-arrow-down"
                trend_color = "var(--error-600)"
            else:
                trend_icon = "fas fa-minus"
                trend_color = "var(--neutral-500)"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">
                <i class="{icon}" style="margin-right: 0.5rem; color: {color_map.get(color, color_map['primary'])};"></i>
                {title}
            </div>
            <div class="metric-value" style="color: {color_map.get(color, color_map['primary'])};">{value}</div>
            {f'<div style="font-size: 0.875rem; color: {trend_color}; margin-top: 0.5rem;"><i class="{trend_icon}"></i> {trend}%</div>' if trend is not None else ''}
            {f'<div style="font-size: 0.875rem; color: var(--neutral-600); margin-top: 0.5rem;">{subtitle}</div>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def modern_card(title, content, icon=None, color="primary"):
        """Create a modern card container"""
        color_map = {
            "primary": "var(--primary-600)",
            "success": "var(--success-600)",
            "warning": "var(--warning-600)", 
            "error": "var(--error-600)",
            "info": "var(--neutral-600)"
        }
        
        st.markdown(f"""
        <div class="modern-card">
            <h3 style="margin: 0 0 1rem 0; color: var(--neutral-800); font-weight: 700; font-size: 1.25rem;">
                {f'<i class="{icon}" style="margin-right: 0.5rem; color: {color_map.get(color, color_map["primary"])};"></i>' if icon else ''}
                {title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def loading_spinner(text="Loading..."):
        """Show a modern loading spinner"""
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <div class="loading-spinner" style="margin-bottom: 1rem;"></div>
            <div style="color: var(--neutral-600); font-weight: 500;">{text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def success_message(message, title="Success"):
        """Show a modern success message"""
        st.markdown(f"""
        <div class="stSuccess">
            <div style="display: flex; align-items: center;">
                <i class="fas fa-check-circle" style="margin-right: 0.75rem; font-size: 1.25rem;"></i>
                <div>
                    <div style="font-weight: 700; margin-bottom: 0.25rem;">{title}</div>
                    <div>{message}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def error_message(message, title="Error"):
        """Show a modern error message"""
        st.markdown(f"""
        <div class="stError">
            <div style="display: flex; align-items: center;">
                <i class="fas fa-exclamation-circle" style="margin-right: 0.75rem; font-size: 1.25rem;"></i>
                <div>
                    <div style="font-weight: 700; margin-bottom: 0.25rem;">{title}</div>
                    <div>{message}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def warning_message(message, title="Warning"):
        """Show a modern warning message"""
        st.markdown(f"""
        <div class="stWarning">
            <div style="display: flex; align-items: center;">
                <i class="fas fa-exclamation-triangle" style="margin-right: 0.75rem; font-size: 1.25rem;"></i>
                <div>
                    <div style="font-weight: 700; margin-bottom: 0.25rem;">{title}</div>
                    <div>{message}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def info_message(message, title="Info"):
        """Show a modern info message"""
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, var(--primary-50) 0%, var(--primary-100) 100%);
                    border: 1px solid var(--primary-200);
                    border-radius: var(--radius-xl);
                    padding: var(--space-6);
                    box-shadow: var(--shadow-lg);
                    margin: var(--space-4) 0;">
            <div style="display: flex; align-items: center;">
                <i class="fas fa-info-circle" style="margin-right: 0.75rem; font-size: 1.25rem; color: var(--primary-600);"></i>
                <div>
                    <div style="font-weight: 700; margin-bottom: 0.25rem; color: var(--primary-700);">{title}</div>
                    <div style="color: var(--primary-700);">{message}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def progress_bar(value, max_value, label=None, color="primary"):
        """Create a modern progress bar"""
        percentage = (value / max_value * 100) if max_value > 0 else 0
        
        color_map = {
            "primary": "var(--primary-500)",
            "success": "var(--success-500)",
            "warning": "var(--warning-500)",
            "error": "var(--error-500)"
        }
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            {f'<div style="font-weight: 600; color: var(--neutral-700); margin-bottom: 0.5rem;">{label}</div>' if label else ''}
            <div style="background: var(--neutral-200); border-radius: var(--radius-full); height: 0.75rem; overflow: hidden;">
                <div style="background: linear-gradient(90deg, {color_map.get(color, color_map['primary'])} 0%, {color_map.get(color, color_map['primary'])} 100%); 
                            height: 100%; width: {percentage}%; border-radius: var(--radius-full); 
                            transition: width var(--transition-normal);"></div>
            </div>
            <div style="text-align: right; font-size: 0.875rem; color: var(--neutral-600); margin-top: 0.25rem;">
                {value:,.0f} / {max_value:,.0f} ({percentage:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def financial_health_gauge(score, title="Financial Health Score"):
        """Create a modern financial health gauge"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 20, 'color': '#1e293b'}},
            delta = {'reference': 70, 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#64748b"},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, 40], 'color': "#fef2f2"},
                    {'range': [40, 70], 'color': "#fef3c7"},
                    {'range': [70, 100], 'color': "#f0fdf4"}
                ],
                'threshold': {
                    'line': {'color': "#ef4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            font={'family': 'Inter, sans-serif'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    @staticmethod
    def modern_button(text, icon=None, variant="primary", key=None):
        """Create a modern button"""
        variant_styles = {
            "primary": "background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 50%, var(--secondary-600) 100%); color: white;",
            "secondary": "background: linear-gradient(135deg, var(--neutral-100) 0%, var(--neutral-200) 100%); color: var(--neutral-700); border: 1px solid var(--neutral-300);",
            "success": "background: linear-gradient(135deg, var(--success-600) 0%, var(--success-700) 100%); color: white;",
            "warning": "background: linear-gradient(135deg, var(--warning-600) 0%, var(--warning-700) 100%); color: white;",
            "error": "background: linear-gradient(135deg, var(--error-600) 0%, var(--error-700) 100%); color: white;"
        }
        
        button_style = f"""
        <style>
        .modern-button-{key} {{
            {variant_styles.get(variant, variant_styles['primary'])}
            border: none;
            border-radius: var(--radius-lg);
            padding: var(--space-4) var(--space-8);
            font-family: var(--font-primary);
            font-weight: 600;
            font-size: 1rem;
            transition: all var(--transition-normal);
            box-shadow: var(--shadow-lg);
            width: 100%;
            cursor: pointer;
        }}
        .modern-button-{key}:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: var(--shadow-2xl);
        }}
        </style>
        """
        
        st.markdown(button_style, unsafe_allow_html=True)
        
        if icon:
            return st.button(f"{icon} {text}", key=key, use_container_width=True)
        else:
            return st.button(text, key=key, use_container_width=True)
    
    @staticmethod
    def feature_highlight(title, description, icon, color="primary"):
        """Create a feature highlight card"""
        color_map = {
            "primary": ("var(--primary-600)", "var(--primary-100)", "var(--primary-200)"),
            "success": ("var(--success-600)", "var(--success-100)", "var(--success-200)"),
            "warning": ("var(--warning-600)", "var(--warning-100)", "var(--warning-200)"),
            "error": ("var(--error-600)", "var(--error-100)", "var(--error-200)")
        }
        
        icon_color, bg_color, border_color = color_map.get(color, color_map["primary"])
        
        st.markdown(f"""
        <div style="background: {bg_color}; border-radius: var(--radius-lg); padding: 1rem; border: 1px solid {border_color}; margin: 0.5rem 0;">
            <i class="{icon}" style="color: {icon_color}; font-size: 1.5rem; margin-bottom: 0.5rem;"></i>
            <div style="font-weight: 600; color: var(--neutral-800); margin-bottom: 0.25rem;">{title}</div>
            <div style="font-size: 0.875rem; color: var(--neutral-600); line-height: 1.4;">{description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def empty_state(title, description, icon, action_button=None):
        """Create an empty state component"""
        st.markdown(f"""
        <div style="text-align: center; padding: 3rem 2rem; background: rgba(255, 255, 255, 0.8); border-radius: var(--radius-xl); border: 2px dashed var(--neutral-300);">
            <i class="{icon}" style="font-size: 3rem; color: var(--neutral-400); margin-bottom: 1rem;"></i>
            <h3 style="color: var(--neutral-700); font-weight: 600; margin: 0 0 0.5rem 0;">{title}</h3>
            <p style="color: var(--neutral-500); margin: 0;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if action_button:
            st.markdown("<br>", unsafe_allow_html=True)
            return st.button(action_button, use_container_width=True)
    
    @staticmethod
    def data_table(data, title=None):
        """Create a modern data table"""
        if title:
            st.markdown(f"""
            <div class="modern-card">
                <h4 style="margin: 0 0 1rem 0; color: var(--neutral-800); font-weight: 600;">
                    <i class="fas fa-table" style="margin-right: 0.5rem; color: var(--primary-600);"></i>
                    {title}
                </h4>
            </div>
            """, unsafe_allow_html=True)
        
        if isinstance(data, pd.DataFrame):
            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write(data)
