import streamlit as st
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

st.title("💧 Water Quality Dashboard with Infographics and Icons")

# Generate fake sensor data
def generate_data(num_readings=50):
    values = [random.randint(50, 600) for _ in range(num_readings)]
    timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=5*i) for i in range(num_readings)]
    df = pd.DataFrame({"Time": timestamps, "Microplastics": values})
    df = df.sort_values("Time")
    return df

data = generate_data()

# Threshold sliders
good_threshold = st.sidebar.slider("Good max microplastics", 0, 600, 200)
moderate_threshold = st.sidebar.slider("Moderate max microplastics", 0, 600, 400)

# Determine status
def get_status(v):
    if v < good_threshold:
        return "Good"
    elif v < moderate_threshold:
        return "Moderate"
    else:
        return "Contaminated"

data["Status"] = data["Microplastics"].apply(get_status)

# Colors and icon URLs for statuses
colors = {"Good": "green", "Moderate": "orange", "Contaminated": "red"}
icons = {
    "Good": "https://cdn-icons-png.flaticon.com/512/414/414969.png",         # green water drop icon
    "Moderate": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",    # orange warning icon
    "Contaminated": "https://cdn-icons-png.flaticon.com/512/564/564619.png"   # red danger icon
}

# Latest reading and status
latest_value = data["Microplastics"].iloc[-1]
latest_status = get_status(latest_value)

# Show latest status with icon
col_icon, col_text = st.columns([1, 6])
with col_icon:
    st.image(icons[latest_status], width=50)
with col_text:
    st.markdown(f"<h2 style='color: {colors[latest_status]};'>Latest Water Status: {latest_status}</h2>", unsafe_allow_html=True)
    st.write(f"Latest Microplastic Reading: {latest_value}")

# Infographic pie chart
status_counts = data["Status"].value_counts()
sizes = status_counts.values
labels = status_counts.index
color_map = [colors[label] for label in labels]

fig1, ax1 = plt.subplots()
explode = [0.05] * len(sizes)
wedges, texts, autotexts = ax1.pie(
    sizes,
    explode=explode,
    labels=labels,
    colors=color_map,
    autopct='%1.1f%%',
    shadow=True,
    startangle=90,
    wedgeprops=dict(edgecolor='w'),
    textprops=dict(color="black", fontsize=10)
)
ax1.set(aspect="equal", title="Water Quality Status Distribution")

# Area chart for microplastic levels
fig2, ax2 = plt.subplots()
ax2.fill_between(data['Time'], data['Microplastics'], color='skyblue', alpha=0.5)
ax2.plot(data['Time'], data['Microplastics'], color='SteelBlue')
ax2.axhline(y=good_threshold, color='green', linestyle='--', label='Good Threshold')
ax2.axhline(y=moderate_threshold, color='orange', linestyle='--', label='Moderate Threshold')
ax2.set_xlabel('Time')
ax2.set_ylabel('Microplastic Level')
ax2.set_title('Microplastic Levels Over Time')
ax2.legend()
plt.xticks(rotation=45)

col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
with col2:
   st.pyplot(fig2)

