# StreamLit-App
Taking the working of AI Agent further by integrating CrewAI framework with StreamLit-App (another framework), which will help us in showing GUI outputs through our inputs.


## Setup

**Clone this repository into your system and create a virtual environment**
```
git clone https://github.com/TryCatchRaunak/StreamLit-App.git
```

**Then install necessary packages into your virtual environment - crewai, crewai-tools, python-dotenv, streamlit**

```
pip install crewai crewai-tools python-dotenv streamlit
```

**Then in order to run the streamlit_app.py file, enter the following command**
```
streamlit run streamlit_app.py
```
**Now open your browser and paste this link**
```
http://localhost:8501
```

## For Port Forwarding

**Use ngrok for port forwarding**

*Install ngrok into your system, then run the following command:*

```
ngrok http <desired_url>
```