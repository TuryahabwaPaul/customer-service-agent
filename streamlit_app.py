import streamlit as st
from streamlit_option_menu import option_menu
from chatbot import Chatbot
import plotly.graph_objects as go
import pandas as pd
import pathlib

# Set page config (move this to the top)
st.set_page_config(page_title="AI Sales Assistant", layout="wide", initial_sidebar_state="expanded", page_icon="💼")

# Load custom CSS function definition
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Use the load_css function to load the styles.css file
load_css("style.css")
# Function to create new object of chatbot
def initialize_chatbot():
    st.session_state['chatbot'] = Chatbot()

# Function to clear chat history by creating a new object of chatbot
def clear_chat_history():
    st.session_state.messages = []
    intro = '''Hello, I'm your AI Sales Assistant. How can I help you boost your sales performance today?'''
    st.session_state.messages.append({"role": "assistant", "content": intro})
    initialize_chatbot()  # Reinitialize the Chatbot instance

# Adding clear history button on sidebar
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Placeholder for logo (replace with your actual logo)
st.sidebar.image("logo.PNG", width=150)

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home", "Sales Dashboard", "Lead Management", "Product Recommendations", "Data Upload", "Settings"],
        icons = ["house", "graph-up", "person-lines-fill", "cart", "cloud-upload", "gear"],
        menu_icon = "cast",
        default_index = 0,
    )

if selected == "Home":
    st.title("AI Sales Assistant")
    
    # Initialize chatbot object
    if "chatbot" not in st.session_state:
        st.session_state['chatbot'] = Chatbot()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        intro = '''Hello, I'm your AI Sales Assistant. How can I help you boost your sales performance today?'''
        st.session_state.messages.append({"role": "assistant", "content": intro})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me anything about sales..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = st.session_state['chatbot'].run_chatbot(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

elif selected == "Sales Dashboard":
    st.title("Sales Dashboard")
    
    # Use RAG to get sales data insights
    sales_query = "Provide a summary of our sales performance and key metrics."
    sales_insights = st.session_state['chatbot'].run_chatbot(sales_query)
    st.write(sales_insights)
    
    # You can still include static visualizations if needed
    sales_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [12000, 15000, 18000, 16000, 22000, 25000]
    })
    
    fig = go.Figure(data=go.Scatter(x=sales_data['Month'], y=sales_data['Sales'], mode='lines+markers'))
    fig.update_layout(title='Monthly Sales Performance', xaxis_title='Month', yaxis_title='Sales ($)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Example: Sales by Product Line
    product_sales = pd.DataFrame({
        'Product Line': ['Electronics', 'Fashion', 'Groceries', 'Health', 'Toys'],
        'Sales': [5000, 8000, 12000, 4000, 2000]
    })
    product_fig = go.Figure(data=go.Pie(labels=product_sales['Product Line'], values=product_sales['Sales']))
    product_fig.update_layout(title='Sales by Product Line')
    st.plotly_chart(product_fig, use_container_width=True)

    

elif selected == "Lead Management":
    st.title("Lead Management")
    
    lead_query = "List our top 5 leads with their scores and provide a brief qualification strategy for each."
    lead_insights = st.session_state['chatbot'].run_chatbot(lead_query)
    st.write(lead_insights)
    
    if st.button("Generate Lead Qualification Plan"):
        plan_query = "Create a detailed lead qualification plan for our sales team."
        qualification_plan = st.session_state['chatbot'].run_chatbot(plan_query)
        st.write(qualification_plan)

elif selected == "Product Recommendations":
    st.title("Product Recommendations")
    
    customer = st.text_input("Enter customer name or ID:")
    if customer:
        rec_query = f"Provide product recommendations for customer: {customer}"
        recommendations = st.session_state['chatbot'].run_chatbot(rec_query)
        st.write(recommendations)

elif selected == "Data Upload":
    st.title("Data Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)
            if st.button("Process and Upload Data"):
                with st.spinner("Processing and uploading data..."):
                    success = st.session_state['chatbot'].process_and_upload_data(dataframe)
                if success:
                    st.success("Data processed and uploaded successfully!")
                else:
                    st.error("An error occurred during data processing and upload. Please check the logs for details.")
        except Exception as e:
            st.error(f"Error reading the CSV file: {str(e)}")

elif selected == "Settings":
    st.title("Settings")
    st.write("Customize your AI Sales Assistant settings here.")
    
    integration = st.checkbox("Enable CRM Integration")
    if integration:
        crm = st.selectbox("Select CRM", ["Salesforce", "HubSpot", "Pipedrive"])
        st.success(f"{crm} integration enabled!")
    
    notification = st.checkbox("Enable Email Notifications")
    if notification:
        st.text_input("Email Address")
        st.success("Email notifications enabled!")

    if st.button("Update Knowledge Base"):
        update_query = "Update the knowledge base with the latest sales strategies and market trends."
        update_result = st.session_state['chatbot'].run_chatbot(update_query)
        st.success("Knowledge base updated successfully!")
        st.write(update_result)
        
    