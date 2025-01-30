import streamlit as st
from streamlit_stl import stl_from_file
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from .cad_files import *
# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    st.error("OpenAI API key not found. Please make sure you have set OPENAI_API_KEY in your .env file.")
    st.stop()

client = OpenAI(api_key=openai_api_key)
# Load the CSV file containing missile data
try:
    missile_data = pd.read_csv('rocket_motor_data.csv')
except FileNotFoundError:
    st.error("rocket_motot_data.csv not found. Please make sure the file exists in the same directory as app.py")
    st.stop()

# Function to find the nearest missile based on user inputs
def find_nearest_missile(payload, range_km, altitude_km, speed_mach):
    # Prepare the query for OpenAI
    query = f"Find the nearest rocket with payload {payload} kg, range {range_km} km, altitude {altitude_km} km, and speed {speed_mach} Mach."
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Always respond with valid JSON."},
            {"role": "user", "content": query + " " + missile_data.to_string() + " Return the result as JSON with rocket_name field."}
        ]
    )
    
    try:
        # Get the content and parse as JSON
        response_content = completion.choices[0].message.content
        result = json.loads(response_content)
        return result.get('rocket_name', 'No rocket found')
    except (json.JSONDecodeError, AttributeError) as e:
        return f"Error processing response: {str(e)}"

def extract_dimensions(rocket_name):
    # Read the CSV file
    missile_data = pd.read_csv('rocket_motor_data.csv')
    
    # Find the row with the matching rocket name
    row = missile_data[missile_data['rocket_name'] == rocket_name]
    
    if row.empty:
        return "Rocket not found"
    
    # Extract the dimensions
    rocket_dimensions = {
        'rocket_name': row['rocket_name'].values[0],
        'payload_mass': row['payload_mass'].values[0],
        'range': row['range'].values[0],
        'altitude': row['altitude'].values[0],
        'speed': row['speed'].values[0],
        'casing_outer_diameter': row['casing_outer_diameter'].values[0],
        'casing_inner_diameter': row['casing_inner_diameter'].values[0],
        'casing_height': row['casing_height'].values[0],
        'bulkhead_hole_diameter': row['bulkhead_hole_diameter'].values[0],
        'bulkhead_outer_diameter': row['bulkhead_outer_diameter'].values[0],
        'bulkhead_thickness': row['bulkhead_thickness'].values[0],
        'bulkhead_height': row['bulkhead_height'].values[0],
        'bulkhead_a': row['bulkhead_a'].values[0],
        'bulkhead_b': row['bulkhead_b'].values[0],
        'grain_outer_diameter': row['grain_outer_diameter'].values[0],
        'grain_inner_diameter': row['grain_inner_diameter'].values[0],
        'grain_height': row['grain_height'].values[0],
        'nozzle_throat_diam': row['nozzle_throat_diam'].values[0],
        'nozzle_exit_diam': row['nozzle_exit_diam'].values[0],
        'nozzle_inlet_diam': row['nozzle_inlet_diam'].values[0],
        'nozzle_outer_diam': row['nozzle_outer_diam'].values[0],
        'nozzle_convergent_angle': row['nozzle_convergent_angle'].values[0],
        'nozzle_divergent_angle': row['nozzle_divergent_angle'].values[0],
        'nozzle_a': row['nozzle_a'].values[0],
        'nozzle_b': row['nozzle_b'].values[0]
    }

    
    return rocket_dimensions

# Streamlit UI
st.set_page_config(layout="wide")
st.title('Missile Builder')

payload = st.number_input('Enter payload in kilograms:', min_value=0)
range_km = st.number_input('Enter range in kilometers:', min_value=0)
altitude_km = st.number_input('Enter altitude in kilometers:', min_value=0)
speed_mach = st.selectbox('Select speed (Mach):', options=[1, 2, 3, 4, 5])
flag = False
if st.button('Find Nearest Missile'):
    nearest_missile = find_nearest_missile(payload, range_km, altitude_km, speed_mach)
    rocket_dimensions = extract_dimensions(nearest_missile)
    st.write('Nearest Missile:')
    st.write(nearest_missile)
    st.write('Rocket Dimensions:')
    st.write(rocket_dimensions)

    # Generate CAD files
   
    flag = generate_cad_files(rocket_dimensions)
stl_files = [f for f in os.listdir('.') if f.endswith('.stl')]
# keys = [f for f in os.listdir('.') if f.endswith('.stl')]
# selected_stl_file = st.selectbox("Select STL file", stl_files, key='selected_stl_file')
st.subheader("Components!")
cols = st.columns(5)
with cols[0]:
    color = st.color_picker("Pick a color", "#FF9900", key='color_file')
with cols[1]:
    material = st.selectbox("Select a material", ["material", "flat", "wireframe"], key='material_file')
with cols[2]:
    st.write('\n'); st.write('\n')
    auto_rotate = st.toggle("Auto rotation", key='auto_rotate_file')
with cols[3]:
    opacity = st.slider("Opacity", min_value=0.0, max_value=1.0, value=1.0, key='opacity_file')
with cols[4]:
    height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_file')

# camera position
cols = st.columns(4)
with cols[0]:
    cam_v_angle = st.number_input("Camera Vertical Angle", value=60, key='cam_v_angle')
with cols[1]:
    cam_h_angle = st.number_input("Camera Horizontal Angle", value=-90, key='cam_h_angle')
with cols[2]:
    cam_distance = st.number_input("Camera Distance", value=0, key='cam_distance')
with cols[3]:
    max_view_distance = st.number_input("Max view distance", min_value=1, value=1000, key='max_view_distance')

stl_files = stl_files[0:4]  # Ensure we only have four files to display
cols = st.columns(len(stl_files))

for i, (col, stl_file) in enumerate(zip(cols, stl_files)):
    with col:
        st.subheader(stl_file)
        stl_from_file(file_path=stl_file, 
                      color=color,
                      material=material,
                      auto_rotate=auto_rotate,
                      opacity=opacity,
                      height=height,
                      shininess=100,
                      cam_v_angle=cam_v_angle,
                      cam_h_angle=cam_h_angle,
                      cam_distance=cam_distance,
                      max_view_distance=max_view_distance,
                      key=f'stl_file_{i}')
