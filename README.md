# AI Sales Assistant 💼

This AI Sales Assistant is a web-based application. It leverages a chatbot to assist users in managing sales activities, viewing sales dashboards, managing leads, and providing product recommendations. The app also supports file uploads for data processing and customizable settings.

![Alt text for the image](https://raw.githubusercontent.com/TuryahabwaPaul/customer-service-agent/main/Screenshot_20241018_133748_Chrome.jpg)


```bash
Url  - https://customer-service-agent.streamlit.app/
```

## Features
- **Chatbot Interaction:** AI-powered chatbot for sales queries and assistance.
- **Sales Dashboard:** Visualizations for sales performance metrics.
- **Lead Management:** View top leads and generate qualification strategies.
- **Product Recommendations:** Suggest products for customers based on their needs.
- **Data Upload:** Upload CSV files for data analysis and processing.
- **Custom Settings:** Customize the app, including CRM integration and notification settings.
- **Clear Chat History:** Reset chat interactions to start fresh.
- **Customizable UI with CSS:** You can style the app with your custom CSS for a tailored look and feel.

## Installation

### Prerequisites
Make sure you have the following installed on your machine:
- Python 3.7+
- Streamlit (`pip install streamlit`)
- Other required Python packages listed in the `requirements.txt` file.

### Clone the Repository
```bash
git clone https://github.com/your-username/ai-sales-assistant.git
cd ai-sales-assistant
```

### Install Dependencies
Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```

### Run the App
Start the app by running the following command in the terminal:
```bash
streamlit run app.py
```

### Access the App
Once the app is running, it will automatically open in your default web browser at:
```
http://localhost:8501
```

### Mobile View
You can simulate the app on a mobile device using Chrome DevTools:
1. Open Chrome.
2. Right-click anywhere on the page and click "Inspect."
3. Click the "Toggle device toolbar" icon to switch to mobile view.
4. Select a device from the dropdown menu or manually set a custom resolution.

## Custom CSS
You can customize the UI theme of the app by editing the `styles.css` file. Here's a breakdown of the current customizations:
- **Body Theme:** Changes the background color, text color, and font.
- **Button Styling:** Customizes button colors and shapes.
- **Text Input Styling:** Adds padding and background color to text input fields.
- **Sidebar:** Modifies the background color and logo display in the sidebar.
- **Graph Styling:** Styles Plotly graphs to match the overall theme.

You can modify this file to fit your branding or personal preferences. To apply the CSS, make sure to include the following in your `app.py`:
```python
st.markdown("<style>{}</style>".format(open('styles.css').read()), unsafe_allow_html=True)
```

## File Structure

```plaintext
.
├── app.py                     # Main Streamlit app file
├── chatbot.py                 # Chatbot logic
├── styles.css                 # Custom CSS for UI theming
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Contributing
Feel free to fork the repository and submit a pull request for any improvements or features you'd like to add.

