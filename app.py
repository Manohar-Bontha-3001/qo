from flask import Flask, request, render_template, redirect, url_for
from azure.storage.blob import BlobServiceClient
import pandas as pd

app = Flask(__name__)

# Azure Blob Storage connection string and container name
AZURE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=manoharb1;AccountKey=LaHIGY//k5jTwvopx10ng/LH1T5hDXE5mV46AgSO7GvQ9HQ/K7RAZjucAJvkgIGETfzC6IuTN5G1+AStqABahg==;EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'manoharb1'

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# Initialize the container
try:
    container_client = blob_service_client.create_container(CONTAINER_NAME)
except Exception as e:
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# In-memory data storage for demonstration purposes
people_df = pd.DataFrame(columns=['Name', 'Salary', 'Room', 'Telnum', 'Picture', 'Keywords'])

@app.route('/')
def index():
    return render_template('index.html', name="Your Name", id="123456")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Upload people.csv
        file = request.files['file']
        if file:
            global people_df
            people_df = pd.read_csv(file)
        
        # Upload pictures
        pictures = request.files.getlist('pictures')
        for pic in pictures:
            blob_client = container_client.get_blob_client(blob=pic.filename)
            blob_client.upload_blob(pic)
        
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_by = request.form['search_by']
        value = request.form['value']
        
        if search_by == 'name':
            result = people_df[people_df['Name'].str.contains(value, case=False, na=False)]
        elif search_by == 'salary':
            min_cost, max_cost = map(int, value.split('-'))
            result = people_df[(people_df['Salary'] >= min_cost) & (people_df['Salary'] <= max_cost)]
        
        result = result.to_dict(orient='records')
        return render_template('search.html', result=result)
    return render_template('search.html')

@app.route('/name_search', methods=['GET', 'POST'])
def name_search():
    if request.method == 'POST':
        name = request.form['name']
        result = people_df[people_df['Name'].str.contains(name, case=False, na=False)].to_dict(orient='records')
        return render_template('name_search.html', result=result)
    return render_template('name_search.html')

@app.route('/cost_search', methods=['GET', 'POST'])
def cost_search():
    if request.method == 'POST':
        min_cost = int(request.form['min_cost'])
        max_cost = int(request.form['max_cost'])
        result = people_df[(people_df['Salary'] >= min_cost) & (people_df['Salary'] <= max_cost)].to_dict(orient='records')
        return render_template('cost_search.html', result=result)
    return render_template('cost_search.html')

@app.route('/update_description', methods=['GET', 'POST'])
def update_description():
    if request.method == 'POST':
        name = request.form['name']
        new_description = request.form['description']
        people_df.loc[people_df['Name'] == name, 'Keywords'] = new_description
        return redirect(url_for('index'))
    return render_template('update_description.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        global people_df
        people_df = people_df[people_df['Name'] != name]
        return redirect(url_for('index'))
    return render_template('delete.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        room = request.form['room']
        telnum = request.form['telnum']
        picture = request.files['picture']
        keywords = request.form['keywords']

        # Upload picture to Azure Blob Storage
        blob_client = container_client.get_blob_client(blob=picture.filename)
        blob_client.upload_blob(picture)

        # Add new user to the DataFrame
        new_user = pd.DataFrame([[name, salary, room, telnum, picture.filename, keywords]], columns=['Name', 'Salary', 'Room', 'Telnum', 'Picture', 'Keywords'])
        global people_df
        people_df = pd.concat([people_df, new_user], ignore_index=True)

        return redirect(url_for('index'))
    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
