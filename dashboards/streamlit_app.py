import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Porter Delivery Analytics | Professional Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional color palette
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#9467bd',
    'accent': '#8c564b',
    'gradient': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
}

# Enhanced professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .section-header {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        font-weight: 500;
        margin: 0;
    }
    
    .recommendation-container {
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #feca57;
    }
    
    .recommendation-card h4 {
        color: #feca57;
        margin-top: 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .impact-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .impact-high { background: #e74c3c; color: white; }
    .impact-medium { background: #f39c12; color: white; }
    .impact-low { background: #3498db; color: white; }
    
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .sidebar .sidebar-content {
    background: black;
    border-radius: 10px;
    padding: 1rem;
    color: white;
    }

    
    .stSelectbox > div > div {
    background-color: black !important;
    color: white !important;
    border-radius: 8px;
    border: 1px solid #444;
}

.stSelectbox > div > div * {
    color: white !important;
}

    
    .footer {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the Porter delivery data from CSV"""
    try:
        # Load the dataset from the specified path
        df = pd.read_csv("porter_cleaned.csv")
        
        # Convert date columns to datetime
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['actual_delivery_time'] = pd.to_datetime(df['actual_delivery_time'])
        
        # Ensure logical constraints
        df['total_busy_partners'] = np.minimum(df['total_busy_partners'], df['total_onshift_partners'])
        df['num_distinct_items'] = np.minimum(df['num_distinct_items'], df['total_items'])
        
        # Calculate derived fields
        df['hour'] = df['created_at'].dt.hour
        df['day_of_week'] = df['created_at'].dt.day_name()
        df['date'] = df['created_at'].dt.date
        df['month'] = df['created_at'].dt.month
        
        # Handle division by zero for partner_utilization and orders_per_partner
        df['partner_utilization'] = np.where(
            df['total_onshift_partners'] > 0,
            df['total_busy_partners'] / df['total_onshift_partners'],
            0
        )
        df['orders_per_partner'] = np.where(
            df['total_onshift_partners'] > 0,
            df['total_outstanding_orders'] / df['total_onshift_partners'],
            0
        )
        
        # Replace any remaining infinite values with 1.0 (100% utilization) or NaN
        df['partner_utilization'] = df['partner_utilization'].replace([np.inf, -np.inf], 1.0)
        df['orders_per_partner'] = df['orders_per_partner'].replace([np.inf, -np.inf], 0)
        
        # Handle NaN values
        df['partner_utilization'] = df['partner_utilization'].fillna(0)
        df['orders_per_partner'] = df['orders_per_partner'].fillna(0)
        
        # Categorize delivery performance based on dataset values
        df['delivery_performance'] = pd.cut(
            df['delivery_duration_minute'], 
            bins=[0, 20, 35, 50, float('inf')], 
            labels=['Excellent (<20min)', 'Good (20-35min)', 'Average (35-50min)', 'Poor (>50min)']
        )
        
        # Price per item
        df['price_per_item'] = np.where(
            df['total_items'] > 0,
            df['subtotal'] / df['total_items'],
            0
        )
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def format_number(num):
    """Convert large numbers to compact K/M/B format"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return f"{num:,.0f}"

def create_kpi_metrics(df):
    """Create professional KPI metrics"""
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_orders = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_number(total_orders)}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_delivery = df['delivery_duration_minute'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_delivery:.1f}min</div>
            <div class="metric-label">Avg Delivery Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_order_value = df['subtotal'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{format_number(total_order_value)}</div>
            <div class="metric-label">Total Order Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_order_value = df['subtotal'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{avg_order_value:.0f}</div>
            <div class="metric-label">Avg Order Value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        utilization = df['partner_utilization'].mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{utilization:.1f}%</div>
            <div class="metric-label">Partner Utilization</div>
        </div>
        """, unsafe_allow_html=True)

def create_delivery_performance_charts(df):
    """Create delivery performance visualizations"""
    st.markdown('<div class="section-header">🚚 Delivery Performance Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Delivery time distribution
        fig = px.histogram(df, x='delivery_duration_minute', nbins=30, 
                         title='Delivery Time Distribution',
                         color_discrete_sequence=[COLORS['primary']])
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='white')
            )
        )
        fig.update_layout(
            height=400, 
            showlegend=False,
            title_x=0.30,
            xaxis_title="Delivery Time (Minutes)",
            yaxis_title="Order Count"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Performance categories pie chart
        perf_counts = df['delivery_performance'].value_counts()
        fig = px.pie(values=perf_counts.values, names=perf_counts.index,
                    title='Delivery Performance Categories',
                    color_discrete_sequence=COLORS['gradient'])
        fig.update_layout(
            height=400,
            title_x=0.25
        )
        st.plotly_chart(fig, use_container_width=True)

def create_category_analysis(df):
    """Create store category analysis with top performers"""
    st.markdown('<div class="section-header">🏪 Store Category Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average delivery time by category (top 5 by volume)
        top_categories = df['store_primary_category'].value_counts().nlargest(5).index
        category_avg = df[df['store_primary_category'].isin(top_categories)].groupby('store_primary_category')['delivery_duration_minute'].mean().sort_values()
        fig = px.bar(x=category_avg.values, y=category_avg.index, orientation='h',
                    title='Top 5 Avg Delivery Time by Category',
                    color=category_avg.values, color_continuous_scale='RdYlBu_r')
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=150, r=20, t=50, b=20),
            font=dict(size=12),
            title_x=0.25,
            yaxis_title="Category",
            xaxis_title="Average Delivery Time (min)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Order volume by category (top 5)
        category_volume = df['store_primary_category'].value_counts().nlargest(5)
        fig = px.bar(x=category_volume.index, y=category_volume.values,
                    title='Top 5 Order Volume by Category',
                    color=category_volume.values, color_continuous_scale='Viridis')
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=100),
            font=dict(size=12),
            title_x=0.25,
            xaxis_title="Category",
            yaxis_title="Order Volume",
            xaxis=dict(tickangle=45)
        )
        st.plotly_chart(fig, use_container_width=True)

def create_time_analysis(df):
    """Create time-based analysis"""
    st.markdown('<div class="section-header">⏰ Time-Based Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly trends
        hourly_data = df.groupby('hour').agg({
            'delivery_duration_minute': 'mean',
            'created_at': 'count'
        }).reset_index()
        hourly_data.columns = ['hour', 'avg_delivery_time', 'order_count']
        
        fig = px.line(hourly_data, x='hour', y='avg_delivery_time',
                     title='Average Delivery Time by Hour',
                     markers=True, color_discrete_sequence=[COLORS['warning']])
        fig.update_layout(
            height=400,
            title_x=0.25,
            xaxis_title="Hour of Day",
            yaxis_title="Average Delivery Time (min)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Day of week analysis
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_data = df.groupby('day_of_week')['delivery_duration_minute'].mean().reindex(day_order)
        
        fig = px.bar(x=day_data.index, y=day_data.values,
                    title='Average Delivery Time by Day',
                    color=day_data.values, color_continuous_scale='Blues')
        fig.update_layout(
            height=400, 
            showlegend=False,
            title_x=0.25,
            xaxis_title="Day of Week",
            yaxis_title="Average Delivery Time (min)"
        )
        st.plotly_chart(fig, use_container_width=True)

def create_operational_metrics(df):
    """Create operational efficiency metrics"""
    st.markdown('<div class="section-header">⚙️ Operational Efficiency</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Partner utilization vs delivery time
        df['util_bins'] = pd.cut(df['partner_utilization'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        util_performance = df.groupby('util_bins')['delivery_duration_minute'].mean()
        
        fig = px.bar(x=util_performance.index, y=util_performance.values,
                    title='Delivery Time vs Partner Utilization',
                    color=util_performance.values, color_continuous_scale='RdYlGn_r')
        fig.update_layout(
            height=400, 
            showlegend=False,
            title_x=0.25,
            xaxis_title="Partner Utilization",
            yaxis_title="Average Delivery Time (min)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Order size impact
        df['size_category'] = pd.cut(df['total_items'], bins=[0, 2, 4, 6, float('inf')], 
                                   labels=['Small (1-2)', 'Medium (3-4)', 'Large (5-6)', 'XL (7+)'])
        size_impact = df.groupby('size_category')['delivery_duration_minute'].mean()
        
        fig = px.bar(x=size_impact.index, y=size_impact.values,
                    title='Delivery Time by Order Size',
                    color=size_impact.values, color_continuous_scale='Oranges')
        fig.update_layout(
            height=400, 
            showlegend=False,
            title_x=0.25,
            xaxis_title="Order Size Category",
            yaxis_title="Average Delivery Time (min)"
        )
        st.plotly_chart(fig, use_container_width=True)

def create_market_analysis(df):
    """Create market-level analysis"""
    st.markdown('<div class="section-header">📍 Market Performance Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 markets by volume
        market_volume = df['market_id'].value_counts().head(10)
        fig = px.bar(x=market_volume.index.astype(str), y=market_volume.values,
                    title='Top 10 Markets by Order Volume',
                    color=market_volume.values, color_continuous_scale='Turbo')
        fig.update_layout(
            height=400, 
            showlegend=False,
            title_x=0.25,
            xaxis_title="Market ID",
            yaxis_title="Order Volume"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Market performance scatter
        market_stats = df.groupby('market_id').agg({
            'delivery_duration_minute': 'mean',
            'subtotal': 'mean',
            'created_at': 'count'
        }).reset_index()
        market_stats = market_stats[market_stats['created_at'] >= 1000]
        
        fig = px.scatter(market_stats, x='delivery_duration_minute', y='subtotal',
                        size='created_at', title='Market Performance: Delivery Time vs Order Value',
                        color='delivery_duration_minute', color_continuous_scale='RdYlBu_r')
        fig.update_layout(
            height=400,
            title_x=0.1,
            xaxis_title="Average Delivery Time (min)",
            yaxis_title="Average Order Value (₹)"
        )
        st.plotly_chart(fig, use_container_width=True)

def create_financial_analysis(df):
    """Create financial performance analysis"""
    st.markdown('<div class="section-header">💰 Financial Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by top 5 categories
        revenue_by_category = df.groupby('store_primary_category')['subtotal'].sum().nlargest(5)
        fig = px.pie(values=revenue_by_category.values, names=revenue_by_category.index,
                    title='Top 5 Revenue by Category',
                    color_discrete_sequence=COLORS['gradient'])
        fig.update_traces(
            textinfo='percent+label',
            marker=dict(line=dict(color='white',width=1)),
            domain=dict(x=[0,1], y=[0,1])
        )
        fig.update_layout(
            height=400,
            title_x=0.25
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Enhanced price per item distribution
        fig = px.histogram(df, x='price_per_item', nbins=30,
                          title='Price per Item Distribution',
                          color_discrete_sequence=[COLORS['success']],
                          opacity=0.8)
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='white'),
                pattern=dict(fillmode='overlay', size=10, solidity=0.2)
            )
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            title_x=0.25,
            xaxis_title="Price per Item (₹)",
            yaxis_title="Order Count",
            plot_bgcolor='black',
            paper_bgcolor='black'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_professional_recommendations(df):
    """Display professional recommendations with enhanced styling"""
    st.markdown("""
    <div class="recommendation-container">
        <div class="section-header">🎯 Strategic Recommendations</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate insights
    peak_hour = df.groupby('hour')['delivery_duration_minute'].mean().idxmax()
    slowest_category = df.groupby('store_primary_category')['delivery_duration_minute'].mean().idxmax()
    high_util_impact = df[df['partner_utilization'] > 0.8]['delivery_duration_minute'].mean()
    low_util_impact = df[df['partner_utilization'] < 0.3]['delivery_duration_minute'].mean()
    
    recommendations = [
        {
            "title": "🚀 Optimize Peak Hour Operations",
            "description": f"Deploy additional partners during hour {peak_hour} when delivery times are highest. Implement dynamic pricing and partner incentives during peak periods.",
            "impact": "High",
            "timeline": "2-3 weeks",
            "roi": "15-20% reduction in delivery time"
        },
        {
            "title": "📊 Category-Specific Optimization",
            "description": f"Focus on {slowest_category} category which shows longest delivery times. Implement specialized handling processes and dedicated partner pools.",
            "impact": "Medium",
            "timeline": "1-2 months",
            "roi": "10-15% improvement in category performance"
        },
        {
            "title": "⚖️ Partner Utilization Balance",
            "description": f"Maintain optimal partner utilization between 60-70%. Current high utilization increases delivery time by {high_util_impact-low_util_impact:.1f} minutes.",
            "impact": "High",
            "timeline": "Ongoing",
            "roi": "20-25% improvement in delivery efficiency"
        },
        {
            "title": "🎯 Market Expansion Strategy",
            "description": "Identify underperforming markets and implement targeted interventions. Consider market consolidation for better efficiency.",
            "impact": "Medium",
            "timeline": "2-3 months",
            "roi": "5-10% overall performance improvement"
        },
        {
            "title": "💡 Technology Integration",
            "description": "Implement AI-powered route optimization and predictive analytics for demand forecasting to reduce delivery times.",
            "impact": "High",
            "timeline": "3-6 months",
            "roi": "25-30% long-term efficiency gains"
        }
    ]
    
    for rec in recommendations:
        impact_class = f"impact-{rec['impact'].lower()}"
        st.markdown(f"""
        <div class="recommendation-card">
            <h4>{rec['title']}</h4>
            <p>{rec['description']}</p>
            <div style="margin-top: 1rem;">
                <span class="impact-badge {impact_class}">Impact: {rec['impact']}</span>
                <span class="impact-badge impact-medium">Timeline: {rec['timeline']}</span>
                <span class="impact-badge impact-low">ROI: {rec['roi']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚛 Porter Delivery Analytics 📦</h1>
        <p>Professional Performance Dashboard | Data-Driven Insights for Operational Excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.error("Unable to load data. Please check your data source.")
        return
    
    # Sidebar filters
    st.sidebar.markdown("### 🔍 Dashboard Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    # Category filter
    categories = ['All Categories'] + sorted(df['store_primary_category'].unique())
    selected_category = st.sidebar.selectbox("Store Category", categories)
    
    # Market filter
    markets = ['All Markets'] + sorted(df['market_id'].unique())
    selected_market = st.sidebar.selectbox("Market ID", markets)
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'] >= date_range[0]) & 
            (filtered_df['date'] <= date_range[1])
        ]
    
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['store_primary_category'] == selected_category]
    
    if selected_market != 'All Markets':
        filtered_df = filtered_df[filtered_df['market_id'] == selected_market]
    
    # Dashboard sections
    create_kpi_metrics(filtered_df)
    create_delivery_performance_charts(filtered_df)
    create_category_analysis(filtered_df)
    create_time_analysis(filtered_df)
    create_operational_metrics(filtered_df)
    create_market_analysis(filtered_df)
    create_financial_analysis(filtered_df)
    show_professional_recommendations(filtered_df)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>Porter Analytics Dashboard</h3>
        <p>Powered by Advanced Analytics | Built for Operational Excellence</p>
        <p>📊 Data-Driven Decisions | 🚀 Optimized Performance | 💼 Professional Insights</p>
        <p class="developer-signature">🔧 Developed by <span>Utkarsh Karambhe</span> | 📍 Data Analyst @ Porter</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()