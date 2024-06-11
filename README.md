# Cloud-Based Picture and Information Storage System

## Description

This is a web application that allows users to upload a CSV file containing meta-information about people and their pictures. The application stores the pictures in Azure Blob Storage and provides a web interface for searching and updating the information.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/cloud_app.git
    cd cloud_app
    ```

2. Install the required Python packages:
    ```bash
    pip install flask azure-storage-blob pandas
    ```

3. Set up your Azure Storage:
    - Obtain your Azure Storage connection string.
    - Create a container in your Azure Storage account.

4. Update `app.py` with your Azure connection string and container name.

5. Run the Flask app:
    ```bash
    python app.py
    ```

6. Access the web interface by opening your browser and going to `http://127.0.0.1:5000`.

## Usage

- **Upload Files**: Go to the "Upload Files" page to upload the `people.csv` file and the corresponding pictures.
- **Search**: Go to the "Search" page to search for people by name or salary.

## Project Structure

