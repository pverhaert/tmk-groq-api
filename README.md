# TMK Groq Chat Application
This project showcases a chat application built with Streamlit that integrates the Groq platform. 
It's designed to offer speedy real-time AI-driven chat functionalities.

## Technologies Used
- Python 3.x
- Streamlit
- Groq API
- dotenv for environment management

## Getting Started

### Prerequisites
Ensure you have Python 3.11 or higher installed on your system. Streamlit and other required packages will be installed via the requirements file.

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/pverhaert/tmk-groq-api.git
    ```
2. Navigate to the project directory:
    ```bash
    cd tmk-groq-api
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
### Obtaining a Groq API Key
To use this application, you'll need an API key from Groq. Visit the [Groq API documentation](https://console.groq.com/docs/quickstart) to learn how to obtain one.

### Setting Up Your Environment
Once you have your API key, you need to set it in your environment:
- Rename `.env.example` to `.env`.
- Open the `.env` file and replace `YOUR_API_KEY_HERE` with your Groq API key.

This step is crucial for the application to interact with Groq's services securely.

## Running the Application
To run the application, use the following command:
    ```bash
    streamlit run main.py
    ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
