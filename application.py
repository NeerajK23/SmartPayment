from flask import Flask,request,jsonify,render_template,flash
import psycopg2
import datetime
from flask_cors import CORS
app=Flask('__name__')

#app.config['SECRET_KEY']='mysecretkey'
CORS(app)

@app.route("/home")
def hello():
    return render_template('app_page.html')
    #return "Hello World 123"

global COUNT 
@app.route("/login",methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
        request_data = request.form
    print(request_data)
    #request_data=request.get_json()
    MOBILE_NUMBER=request_data['mobile_number']
    PASSWORD=request_data['password']
    try:
        conn = psycopg2.connect("dbname='hacknight' user='postgres' host='0.0.0.0' password='newpassword' port='5432'")
        #conn = psycopg2.connect("dbname='database_name' user='username' host='hostip' password='password'")
        print("Connection OK")
    except:
        print ("Connection Failed")

    cur = conn.cursor()
    #Writing requeried Queries
    cur.execute("""SELECT password FROM vendors where mobile_number ='"""+ MOBILE_NUMBER +"""';""")
    rows = cur.fetchall()
    if len(rows)==0:
        flash('Vendor Not Found', 'success')
        return redirect(url_for('login'))
    else:
        if rows[0][0]==PASSWORD:
            COUNT=MOBILE_NUMBER
            return "Vendor Login Successfully"
            
            #return render_template("home.html",email=email)    
        else:
            return "Wrong Password. Login Again"




@app.route("/transactions", methods=['POST'])
def transactions():
    if request.method == 'POST':
      request_data = request.form    
    #request_data=request.get_json()
    MOBILE_NUMBER=request_data['mobile_number']
    try:
        conn = psycopg2.connect("dbname='hacknight' user='postgres' host='0.0.0.0' password='newpassword' port='5432'")
        #conn = psycopg2.connect("dbname='database_name' user='username' host='hostip' password='password'")
        print("Connection OK")
    except:
        print ("Connection Failed")

    cur = conn.cursor()
    #Writing requeried Queries

    cur.execute("""SELECT aadhar_number,account_number FROM users where mobile_number ='"""+ MOBILE_NUMBER +"""';""")
    rows = cur.fetchall()
    if len(rows)==0:
        return jsonify("User is Not Registered")
    else:
        return jsonify("User Verified")
        #if rows==PASSWORD:
        #    return "User Login Successfully"
            #return render_template("home.html",email=email)
        #else:
        #    return "Login Again"
    

@app.route("/transactionsuccess", methods=['POST'])
def transactionsuccess():
    if request.method == 'POST':
        request_data = request.form
    MOBILE_NUMBER=request_data['mobile_number']
    AMOUNT=request_data['amount']
    COUNT=request_data['from_user']
    now = datetime.datetime.now()
    DATE=now.strftime("%Y-%m-%d %H:%M:%S")
    STATUS='Success'
    MODE='Finger Scanner Device'
    try:
        conn = psycopg2.connect("dbname='hacknight' user='postgres' host='0.0.0.0' password='newpassword' port='5432'")
        #conn = psycopg2.connect("dbname='database_name' user='username' host='hostip' password='password'")
        print("Connection OK")
    except:
        print ("Connection Failed")
    cur = conn.cursor()
    #Writing requeried Queries
    postgres_insert_query=""" INSERT INTO transactions (from_user,to_user,amount,status,mode,date) VALUES (%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (MOBILE_NUMBER,COUNT,AMOUNT,STATUS,MODE,DATE)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify("Transaction Successfully")

@app.route("/gethistory", methods=['POST'])
def gethistory():
    if request.method == 'POST':
        request_data = request.form
    else:    
        request_data = request.get_json()    
    COUNT=request_data['mobile_number']  
    try:
        conn = psycopg2.connect("dbname='hacknight' user='postgres' host='0.0.0.0' password='newpassword' port='5432'")
        #conn = psycopg2.connect("dbname='database_name' user='username' host='hostip' password='password'")
        print("Connection OK")
    except:
        print ("Connection Failed")

    cur = conn.cursor()
    #Writing requeried Queries

    cur.execute("""SELECT * FROM transactions where to_user ='"""+ COUNT +"""' or from_user='"""+ COUNT +"""';""")
    rows = cur.fetchall()
    #print(rows)
    if len(rows)==0:
        return "User is Not Registered"
    else:
        dic1=[]

        for i in range(len(rows)):
            dic={}
            #print(rows[0][0])
            dic["transaction_id"]=rows[i][0]
            dic["from_user"]=rows[i][1]
            dic["to_user"]=rows[i][2]
            dic["amount"]=rows[i][3]
            dic["status"]=rows[i][4]
            dic["date"]=rows[i][6]
            dic1.append(dic)
        print(dic1)    
        #return render_template("app_page.html",forecasted_data = jsonify(forecasted_data))
        return jsonify(dic1)
    

@app.route("/logout")
def logout():
    COUNT=0
    return 


@app.route("/userregister",methods=['POST'])
def userregister():
    if request.method == 'POST':
      request_data = request.form
    #request_data=request.get_json()
    #print(request_data)
    MOBILE_NUMBER=request_data['mobile_number']
    AADHAR_NUMBER=request_data['aadhar_number']
    ACCOUNT_NUMBER=request_data['account_number']
    FNAME=request_data['fname']
    LNAME=request_data['lname']
    IFSC_CODE=request_data['ifsc_code']
    BANK_NAME=request_data['bank_name']
    EMAIL_ID=request_data['email_id']
    PASSWORD=request_data['password']
    try:
        conn = psycopg2.connect("dbname='hacknight' user='postgres' host='0.0.0.0' password='newpassword' port='5432'")
        #conn = psycopg2.connect("dbname='database_name' user='username' host='hostip' password='password'")
        print("Connection OK")
    except:
        print ("Connection Failed")

    cur = conn.cursor()
    #Writing requeried Queries
    postgres_insert_query=""" INSERT INTO users (mobile_number,aadhar_number,account_number,fname,lname,ifsc_code,bank_name,email_id,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (MOBILE_NUMBER,AADHAR_NUMBER,ACCOUNT_NUMBER,FNAME,LNAME,IFSC_CODE,BANK_NAME,EMAIL_ID,PASSWORD)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify("User Registered Successfully")
    #cur.execute("""SELECT password FROM employeedetail where employgmail ='"""+ email +"""' ;""")

@app.route("/vendorregister",methods=['POST'])
def vendorregister():
    if request.method == 'POST':
      request_data = request.form
    
    MOBILE_NUMBER=request_data['mobile_number']
    AADHAR_NUMBER=request_data['aadhar_number']
    ACCOUNT_NUMBER=request_data['account_number']
    FNAME=request_data['fname']
    LNAME=request_data['lname']
    IFSC_CODE=request_data['ifsc_code']
    BANK_NAME=request_data['bank_name']
    EMAIL_ID=request_data['email_id']
    TIN=request_data['tin']
    PAN=request_data['pan']
    PASSWORD=request_data['password']
    try:
        conn = psycopg2.connect("dbname='hacknight' user='postgres' host='0.0.0.0' password='newpassword' port='5432'")
        #conn = psycopg2.connect("dbname='database_name' user='username' host='hostip' password='password'")
        print("Connection OK")
    except:
        print ("Connection Failed")

    cur = conn.cursor()
    #Writing requeried Queries
    postgres_insert_query=""" INSERT INTO vendors (mobile_number,aadhar_number,account_number,fname,lname,ifsc_code,bank_name,email_id,tin,pan,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (MOBILE_NUMBER,AADHAR_NUMBER,ACCOUNT_NUMBER,FNAME,LNAME,IFSC_CODE,BANK_NAME,EMAIL_ID,TIN,PAN,PASSWORD)
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify("Vendor Registered Successfully")
    

if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0',port='5599',  threaded=True)
