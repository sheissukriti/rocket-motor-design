# Rocket Motor Design

This project is a web application for designing and visualizing rocket motors. It allows users to input specific parameters for a rocket and find the nearest matching design from a dataset. The application also generates CAD files for the rocket components using the `cadquery` library.

## Features

- **User Input**: Enter payload, range, altitude, and speed to find the nearest matching rocket design.
- **OpenAI Integration**: Uses OpenAI's API to process and find the best match for the given parameters.
- **CAD File Generation**: Automatically generates CAD files for the rocket components.
- **3D Visualization**: Visualize the rocket components in 3D using Streamlit and `streamlit_stl`.

## Requirements

- Python 3.7 or higher
- The following Python packages:
  - `streamlit`
  - `streamlit_stl`
  - `openai`
  - `pandas`
  - `python-dotenv`
  - `opencv-python`
  - `cadquery`

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/rocket-motor-design.git
   cd rocket-motor-design
   ```

2. **Install Python 3.11.9**:
   Follow the instructions on the official Python website to download and install Python 3.11.9 for your operating system.

3. **Create a Virtual Environment**:
   Create a virtual environment to manage dependencies.
   ```bash
   python -m venv venv

   source venv/bin/activate  #for linux/mac
   
   venv\Scripts\activate.bat  #for windows
   ```

4. **Install Dependencies**:
   Use the `requirements.txt` file to install all necessary packages.
   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. **Run the Application**:
   Start the Streamlit app by running the following command:
   ```bash
   streamlit run app.py
   ```

2. **Input Parameters**:
   - Enter the desired payload, range, altitude, and speed.
   - Click "Fiind Nearest Rocket Motor " to get the closest matching rocket design.

3. **View Results**:
   - The application will display the nearest missile and its dimensions.
   - CAD files for the rocket components will be generated and saved in the current directory.

4. **3D Visualization**:
   - Use the Streamlit interface to visualize the generated STL files.
   - Customize the view with color, material, rotation, opacity, and camera settings options.

## File Structure

- `app.py`: Main application file for the Streamlit app.
- `cad_files.py`: Contains functions to generate CAD files for rocket components.
- `requirements.txt`: Lists all Python dependencies.
- `README.md`: Detailed documentation for the project.


## Contact

For any questions or issues, please contact [info@spacefields.in](mailto:info@spacefields.in).


