from flask import Flask, request,jsonify
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from collections import OrderedDict
from flask_mysqldb import MySQL

#----------Preprocessing----------------------------
df = pd.read_excel('A.L.I2.xlsx')
df =df.fillna(0)
df_new = df.iloc[:,1:]
#---------------------**------------------------------


#----------------------config-------------------------
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'test'
cors = CORS(app,resources={r'/*': {'origins': '*'}}, supports_credentials=True)
mysql = MySQL(app)
#--------------***end of config***--------------------



#-----------------Recommender Function----------------------
def get_recommendations(user_inputs,df_input):
    user_interactions = np.array(user_inputs)

    similarity_scores = cosine_similarity(user_interactions.reshape(1, -1), df_new)
    recommended_items = np.argsort(similarity_scores)[0][::-1]  # reverse sort order

    result = []
    for item in recommended_items:
        result_dict= OrderedDict()
        similarity_percent = similarity_scores[0][item] * 100
        index_number = df.index[df['Apartments']==df.iloc[item,0]].tolist()[0]
        result_dict["index"] = index_number
        result.append(result_dict)
    
    new_result = {}
    
    for i in range(len(result)):
        index_str = 'index'+str(i)
        new_result[index_str] = result[i]["index"]
    
    return new_result

#-------------End of Recommender -------------

@app.route('/',methods=['GET'])
def home():
    return 'Hello. This is home.'

@app.route('/api/v2/recommender',methods=['POST'])
def get_apartments():
    data = request.json
    all_answers=[]
    for part in data:
        all_answers.extend(data[part])

    inputs = {}
    for col in df_new.columns:
        inputs[col] = 0
        if(col in all_answers):
            inputs[col] = 1
    
    user_inputs = [i for i in inputs.values()]
    cursor = mysql.connection.cursor() 
   
    cursor.execute("""SELECT * FROM apartments""")
    rows = cursor.fetchall()
    my_df = pd.DataFrame(rows, columns=[column[0] for column in cursor.description])
    df_cleaned = my_df.iloc[:,1:]
   
    result = get_recommendations(user_inputs,df_cleaned)
    return jsonify(result)


@app.route('/api/v1/recommender', methods=['POST'])
def ocr_result():
    
    data = request.json
    all_answers=[]
    for part in data:
        all_answers.extend(data[part])

    inputs = {}
    for col in df_new.columns:
        inputs[col] = 0
        if(col in all_answers):
            inputs[col] = 1
    
    user_inputs = [i for i in inputs.values()]
    
    #user_inputs = [0,0,1,1,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,1,0,0,1,1,1,1,0,0,1,0,1] # this is only for testing
    new_result = get_recommendations(user_inputs,df)

    return jsonify(new_result)

    

if __name__ == '__main__':
    app.run(debug=True)