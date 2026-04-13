import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Weather Prediction",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Real-Time Weather Prediction")
st.subheader(" Check your city’s weather forecast with live data!")

city = st.text_input("Search your city:", placeholder="Delhi, Mumbai, Bareilly, Shahjahanpur...")

if st.button(" See Weather! 🔍"):
    if city:
        with st.spinner("Data is fetching ..."):
            try:
                response = requests.get(f"http://127.0.0.1:5000/predict?city={city}")  # Flask API se connect kiya
                data = response.json()

                if "error" in data:
                    st.error(f"❌ {data['error']}")
                else:
                    st.success(f"✅ {data['city']} 's Weather!")

                    # Live Weather Display
                    st.markdown("### 🌡️ Todays Live Weather")
                    c = data['current']
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("🌡️ Temp", f"{c['temp']}°C")
                    col2.metric("💧 Humidity", f"{c['humidity']}%") 
                    col3.metric("💨 Wind", f"{c['wind']} km/h")
                    col4.metric("🌧️ Rain", f"{c['rain']} mm")
                    col5.metric("☁️ Cloud", f"{c['cloud']}%")

                    st.markdown("---")

                    # Forecast Display 
                    st.markdown("### 🔮 Future Forecast")
                    cols = st.columns(4)

                    for i, day in enumerate(data['forecast']):
                        date = (datetime.now() + timedelta(days=i+1)).strftime("%d %b")
                        with cols[i]:
                            st.markdown(f"**📅 Day {day['day']} — {date}**")
                            st.metric("🌡️ Temp", f"{day['temp']}°C")
                            st.metric("💧 Humidity", f"{day['humidity']}%")
                            st.metric("💨 Wind", f"{day['wind']} km/h")
                            st.metric("🌧️ Rain", f"{day['rain']} mm")

            except Exception as e:
                st.error(f"❌Error : flask server is running ,cannot connected to API {e}")
    else:
        st.warning("⚠️ Search your city!")