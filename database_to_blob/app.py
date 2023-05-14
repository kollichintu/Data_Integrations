from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib,datetime,json, time
from azure.storage.blob import ContainerClient

start_time = time.time()
#Installation of Flask
app = Flask(__name__)

#set db connection
params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=AGN-CL-LAXMANK-\SQLEXPRESS;DATABASE=testDB;Trusted_Connection=yes;')

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#blob connection
my_connection = "DefaultEndpointsProtocol=https;AccountName=myblobstorage2023;AccountKey=hbB6ogTZ3x/OxACfxVX0JRLxlAHXbGJe1PGKQYzsHYJRPpwqlx/JJ0NofhplWBdujh/Vj2ajOPjx+AStpR27GQ==;EndpointSuffix=core.windows.net"
my_container = "mycontainer2023"
container_client = ContainerClient.from_connection_string(conn_str=my_connection, container_name=my_container)


#instance db object
db = SQLAlchemy(app)

#instantiate marshmallow object
ma = Marshmallow(app)

class Employee(db.Model):
    __tablename_ = 'employee'
    
    Emp_id = db.Column(db.Integer, primary_key=True)
    Emp_Name = db.Column(db.String(200), nullable=False)
    Salary = db.Column(db.String(200), nullable=False)
    Create_Timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#create Employee Schema 
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('Emp_id','Emp_Name', 'Salary', 'Create_Timestamp')

#create instance of schema
employee_schema = EmployeeSchema(many=False)
employees_schema = EmployeeSchema(many=True)
        
# get all employees from DB 
@app.route('/employee', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result_set = employees_schema.dump(employees)
    jsonString = json.dumps(result_set)
    
    jsonFile = open("employee_data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    
    # Upload file
    input_file_path = "./employee_data.json"
    output_blob_name = "SQL_Emp_Data.json"

    with open(input_file_path, "rb") as data:
        container_client.upload_blob(name=output_blob_name, data=data)
        
    
    end_time = time.time() 
    
    total_time = end_time - start_time
    print("Total time taken is= " , total_time)
    return jsonify(result_set)


if __name__ == '__main__':
    app.run(debug=True)