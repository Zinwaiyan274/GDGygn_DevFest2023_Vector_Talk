from flask import Flask, request,jsonify
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from collections import OrderedDict


#----------Preprocessing----------------------------
df = pd.read_excel('A.L.I2.xlsx')
df =df.fillna(0)
df_new = df.iloc[:,1:]
#---------------------**------------------------------


#----------------------config-------------------------
app = Flask(__name__)
cors = CORS(app)

#--------------***end of config***--------------------


@app.route('/api/recommender', methods=['POST'])
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

    return jsonify(new_result)

    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)