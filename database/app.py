from flask  import Flask,jsonify,request


#instance of flask application
app = Flask(__name__)

               
@app.route('/fetchsql', methods= ['POST'])
def fetchsql():  
    
    try:
        custom_query = []
         
        tablename = request.json["tablename"]
        attributes = request.json["attributes"]
        
          
        if  attributes:
            custom_query = f'select {attributes}, {get_aggregations(request.json["aggregations"])}   from {tablename} GROUP BY {attributes}'
        else:
            custom_query = f'select {get_aggregations(request.json["aggregations"])} from {tablename}'
    
        return custom_query
        
        
    except Exception as e:
        return jsonify({"Error": e})
    
   
def get_aggregations(dict):
    result_query =  ", ".join(["(".join([str(val), key+")" +' ' + 'as' +' ' + key]) for key, val in dict.items()])  
    return result_query  