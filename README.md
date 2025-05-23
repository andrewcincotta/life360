# Life360 Web UI

A simple Flask-based web interface to interact with Life360 data.

## Features

- View location data from Life360
- Display member details on a clean web UI
- Flask backend with dynamic routing

## Requirements

- Python 3.8+
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/life360-web-ui.git
    cd life360-web-ui
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment (if needed)**  
   If your app uses a `.env` file or config for API keys or credentials, document that here:

    ```bash
    cp .env.example .env
    # Then edit .env with your API keys
    ```

5. **Run the Flask app**:

    ```bash
    python server.py
    ```

6. **Visit in your browser**:

    ```
    http://localhost:5000
    ```

## Project Structure
tbd 
