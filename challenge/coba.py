from http.client import responses
import re
import sqlite3
import csv
import pandas as pd
from flask import Flask, jsonify, request, make_response
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# database con
data_base=sqlite3.connect('data.db',check_same_thread=False)
data_base.row_factory = sqlite3.Row
mycursor = data_base.cursor()
data_base.execute('''CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT,
old_text varchar(255),
new_text varchar(255));''')

# swager confg
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL , 
    API_URL,
    config={
        'app_name':"app1"
    }
)
# register app
app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix = SWAGGER_URL)

# welcome pages
@app.route('/',methods=['GET'])
def get():
    return "WELCOME TO APP 1"

@app.route('/data',methods=['POST'])
def data():
    if request.method == "POST":
        text = str(request.form["text"])
        text_clean = re.sub(r'[^a-z0-9]',' ',text)
        query_text = "insert into data(old_text,new_text) values(?,?)"
        val = (text,text_clean)
        mycursor.execute(query_text,val)
        data_base.commit()
        # print(text)
        # print(text_clean)

        json_response = {
        'data':[text_clean],
        'description': "Teks yang sudah diproses",
        'status_code': 200,
        }
        response_data = jsonify(json_response)
        return response_data

@app.route("/data/csv", methods=["POST"])
def input_csv():
  if request.method == 'POST':
    file = request.files['file']

    # try:
    data = pd.read_csv(file, encoding='iso-8859-1')
    # data_list = data.values.tolist()
    clean_data_list = []
    
    for i in data_list:
        clean_data_list.append(re.sub(r'[^a-z0-9]',' ',data_list[i]))
        query_text = "insert into data(old_text,new_text) values(?,?)"
        val = (data,clean_data_list)
        mycursor.execute(query_text,val)
        data_base.commit()
    # lst = []
    # for i in data.index:
    #     datacsv = {}
    #     datacsv['?'] = data['?'][i]
    #     datacsv['?'] = data['?'][i]
    #     lst.append(datacsv)
    # csvdata = pd.read_csv
    # except:
    #   data = pd.read_csv(file, encoding='utf-8')
    # (data)]
    # csv_read = csv.DictReader(data)
    # for row in data:
    #     file.append(row)
    
    # text_clean = re.sub(r'[^a-z0-9]',' ',data)
    
    json_response = {
        'data':[text_clean],
        'description': "Teks yang sudah diproses",
        'status_code': 200,
        }
    # for column in data.columns:
    #     data[column] = data[column].str.replace(r'\W',"")
    
    # data.to_csv("cleancsv.csv")

    response_data = jsonify(json_response)
    return response_data

@app.errorhandler(400)
def handle_400_error(_error):
    "return sebuah http 400 error kepada client"
    return make_response(jsonify({'error':'Misunderstood'}),400)

@app.errorhandler(401)
def handle_401_error(_error):
    "return sebuah http 401 error kepada client"
    return make_response(jsonify({'error':'Unauthorised'}),401)

@app.errorhandler(404)
def handle_401_error(_error):
    "return sebuah http 404 error kepada client"
    return make_response(jsonify({'error':'Not Found'}),404)

@app.errorhandler(500)
def handle_401_error(_error):
    "return sebuah http 500 error kepada client"
    return make_response(jsonify({'error':'Server error'}),500)

if __name__ == '__main__':
    app.run(debug=True)
