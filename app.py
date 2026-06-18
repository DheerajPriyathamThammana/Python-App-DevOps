import streamlit as st
import psutil
import os
import time
import pandas as pd
from datetime import datetime

# Page Configuration for a clean, modern UI
st.set_page_config(
    page_title="DevOps Practice Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for extra polish
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allowed_html=True)

st.title("⚙️ DevOps Practice & Monitoring Dashboard")
st.caption("A clean, production-ready UI for practicing containerization, CI/CD, and monitoring.")

# --- SIDEBAR: System Info & Controls ---
st.sidebar.header("Deployment Info")
st.sidebar.info(
    f"""
    **Environment:** {os.getenv('APP_ENV', 'Development')}  
    **Hostname:** {os.getenv('HOSTNAME', 'Localhost')}  
    **Python Version:** 3.x  
    """
)

if st.sidebar.button("Simulate App Crash (Exit)"):
    st.sidebar.error("Triggering container exit...")
    time.sleep(1)
    os._exit(1) # Great for testing Docker restart policies!

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["📊 System Metrics", "📜 Log Analyzer", "🌐 Env Variables"])

# TAB 1: System Metrics (Mock Monitoring)
with tab1:
    st.header("Real-time Server Metrics")
    st.write("Simulating basic infrastructure monitoring (Prometheus/Grafana style).")
    
    col1, col2, col3 = st.columns(3)
    
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    col1.metric(label="CPU Usage", value=f"{cpu_usage}%", delta="-2%" if cpu_usage < 50 else "+5%")
    col2.metric(label="RAM Usage", value=f"{ram_usage}%", delta="0%")
    col3.metric(label="Disk Space", value=f"{disk_usage}%")

    # Simple Health Check Endpoint simulation
    st.subheader("Health Check Status")
    if cpu_usage < 85 and ram_usage < 90:
        st.success("🟢 HTTP 200 OK - Application is Healthy")
    else:
        st.warning("🟡 HTTP 503 - System Under Heavy Load")

# TAB 2: Log Analyzer
with tab2:
    st.header("Log Generation & Parsing")
    st.write("Generate mock application logs to practice log rotation, Fluentd, or ELK stack ingestion.")
    
    log_level = st.selectbox("Select Log Level to Generate", ["INFO", "WARNING", "ERROR"])
    log_message = st.text_input("Log Message", value="User authentication successful.")
    
    if st.button("Write to Log File"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{log_level}] {log_message}\n"
        
        with open("app.log", "a") as f:
            f.write(log_line)
        st.toast("Log written to app.log!", icon="📝")

    # Display current logs
    st.subheader("Recent Logs (`app.log`)")
    if os.path.exists("app.log"):
        with open("app.log", "r") as f:
            logs = f.readlines()[-10:] # Show last 10 logs
        st.code("".join(logs), language="text")
    else:
        st.info("No logs generated yet. Click the button above to create some.")

# TAB 3: Environment Variables
with tab3:
    st.header("Environment Config Checker")
    st.write("Practice injecting variables via `docker run -e` or Kubernetes ConfigMaps.")
    
    # Let users search or view environment variables
    env_data = [{"Variable": k, "Value": v} for k, v in os.environ.items()]
    df = pd.DataFrame(env_data)
    
    search = st.text_input("Filter variables (e.g., PATH, APP_ENV):")
    if search:
        df = df[df['Variable'].str.contains(search, case=False)]
        
    st.dataframe(df, use_container_width=True)
