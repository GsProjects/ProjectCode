from flask import Flask, render_template, request,json,session
from currentLocation import location
from register import register
from changePassword import change_password
from connector import create_connection
from login import login
from animalProfile import add_animal
from analyse_paths import analyse
from update_gps_config import associated_animals
from update_animal_profile import get_animal_profiles
from update_details import update_animal_details
from delete_animal import remove_profiles
from graph_movement import get_graph_details
from graph_data import graph_info
import random


global session
app = Flask(__name__)
app.secret_key=str(random.getrandbits(256))


@app.route('/register',methods=['POST','GET'])
def func():
    x='You are in register'
    print(x)
    global session

    tempUser = request.form['registerUserName'].lower()
    print('tempUser ' + tempUser)
    tempPassword = request.form['registerUserPassword'].lower()
    tempConfirmedPassword = request.form['confirmRegisterUserPassword'].lower()
    if session['loggedIn'] != 'true':
        result = register(tempUser,tempPassword,tempConfirmedPassword)
        for k,v in json.loads(result).items():
            if v == 'ok':
                session['user'] = username
                session['userPassword'] = password
                session['loggedIn'] = 'true'
                return result
            else:
                session['user'] = ''
                session['userPassword'] = ''
                session['loggedIn'] = 'false'
                return result
    else:
        overallResult = json.dumps({"status": "You are already logged in as another user"})
        return overallResult

    
@app.route('/changePassword',methods=['POST','GET'])
def func2():
    x='You are in change password'
    print(x)
    global session

    user = request.form['changeUserName'].lower()
    oldPassword = request.form['oldUserPassword'].lower()
    password = request.form['changeUserPassword'].lower()
    confirmedPassword = request.form['confirmChangeUserPassword'].lower()

    result = change_password(user, password, confirmedPassword, oldPassword )
    for k,v in json.loads(result).items():
        if v == 'updated':
            session['user'] = user
            session['userPassword'] = password
            session['loggedIn'] = 'true'
            return result
        else:
            session['user'] = ''
            session['userPassword'] = ''
            session['loggedIn'] = 'false'
            return result


@app.route('/userlogin',methods=['POST','GET'])
def func3():
    x='You are in login'
    print(x)
    global session

    username = request.form['userName'].lower()
    password = request.form['userPassword'].lower()

    result = login(username,password)
    for k,v in json.loads(result).items():
        if v == 'successful':
            session['user'] = username
            session['userPassword'] = password
            session['loggedIn'] = 'true'
            return result
        else:
            return result

        
@app.route('/animalProfile',methods=['POST','GET'])
def func4():
    x='You are in animalProfile'
    print(x)
    global session

    animalIdentifier = request.form['animalID'].lower()
    animalType= request.form['animalType'].lower()
    animalBreed = request.form['animalBreed'].lower()
    animalWeight = request.form['animalWeight'].lower()
    animalGender= request.form['animalGender'].lower()
    trackingNumber = request.form['trackingNum']
    owner = session['user']

    print("THE SESSION USERNAME IS : " + owner)

    if(session['loggedIn'] == 'true'):
        result = add_animal(animalIdentifier,animalType,animalBreed,animalWeight,animalGender,trackingNumber,owner)    
        return result
    else:
        overallResult = json.dumps({"status": "Session timed out, please log in again"})
        return overallResult

    
@app.route('/currentLocation',methods=['POST','GET'])
def func5():
    x='You are in currentLocation'
    print(x)
    result = location(session['user'])
    
    return json.dumps(result)#mysql datetime objects not json serializeable


@app.route('/analyse_paths',methods=['POST','GET'])
def func6():
    x='You are in analyse_paths'
    print(x)
    global session
    if session['loggedIn'] == 'true':
        animalIdentifier = request.form['animal'].lower()
        trackingNumber = request.form['trackingNum']

        second_animalIdentifier = request.form['animalTwo'].lower()
        second_trackingNumber = request.form['trackingNumTwo']
        #start_date = request.form['date']
        
        result = analyse(animalIdentifier,trackingNumber,second_animalIdentifier,second_trackingNumber,session['user'])
        if result != '':
            return json.dumps(result)
        else:
            return json.dumps({'status':'No Animal Selected'})
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult
        


@app.route('/logout',methods=['POST','GET'])
def func7():
    global session
    print(session['loggedIn'])
    if session['loggedIn'] == 'true':
        session['loggedIn'] = 'false'
        overallResult = json.dumps({"status": "You have logged out successfully"})
        return overallResult
    else:
        overallResult = json.dumps({"status": "Logout failed"})
        return overallResult
    
    
@app.route('/update_gps',methods=['POST','GET'])
def func8():
    global session
    print('In update gps')
    if session['loggedIn'] == 'true':
        result = associated_animals(session['user'])
        if result != [[]]:
            return json.dumps(result)
        else:
            overallResult = json.dumps({"status": "No animals"})
            return overallResult      
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult
        
        
@app.route('/update_animals',methods=['POST','GET'])
def func9():
    global session
    print('In update animals')
    if session['loggedIn'] == 'true':
        result = get_animal_profiles(session['user'])
        if len(result) != 0:
            return json.dumps(result)
        else:
            overallResult = json.dumps({"status": "No animals"})
            return overallResult      
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult
    
    
@app.route('/update_animals_details',methods=['POST','GET'])
def func10():
    global session
    print('In update animals details')
    animalIdentifier = request.form['animalID'].lower()
    animalType= request.form['animalType'].lower()
    animalBreed = request.form['animalBreed'].lower()
    animalWeight = request.form['animalWeight'].lower()
    animalGender= request.form['animalGender'].lower()
    trackingNumber = request.form['trackingNum']
    oldtrackingNumber = request.form['oldTrackingId']
    oldanimalIdentifier = request.form['oldanimalIdentifier'].lower()

    if session['loggedIn'] == 'true':
        result = update_animal_details(animalIdentifier,animalType,animalBreed,animalWeight,animalGender,trackingNumber,oldtrackingNumber,oldanimalIdentifier,session['user'])
        return result
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult
    
            
@app.route('/delete_details',methods=['POST','GET'])
def func11():
    global session
    print('In delete_details')
    animalIdentifier = request.form['animal'].lower()
    trackingNumber = request.form['trackingNum']
    
    if session['loggedIn'] == 'true':
        result = remove_profiles(animalIdentifier, trackingNumber, session['user'])
        return result     
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult

    
@app.route('/get_animal_data',methods=['POST','GET'])
def func12():
    global session
    print('In graph details')
    
    if session['loggedIn'] == 'true':
        result = get_graph_details(session['user'])
        print(result)
        if len(result) != 0:
            return json.dumps(result)
        else:
            overallResult = json.dumps({"status": "No animals"})
            return overallResult      
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult
    
    
@app.route('/get_graph_data',methods=['POST','GET'])
def func13():
    global session
    print('In graph data')
    animalIdentifier = request.form['animal'].lower()
    trackingNumber = request.form['trackingNum']

    if session['loggedIn'] == 'true':
        result = graph_info(animalIdentifier,trackingNumber,session['user'])
        print(result)
        return json.dumps(result)   
    else:
        overallResult = json.dumps({"status": "Your session has timed out, please log in again"})
        return overallResult
    

@app.route('/test',methods=['POST','GET'])
def func14():
    global session
    print('In TEST')
    payload = request.get_data()
    print('payload: ' + str(payload))

    
if __name__ == "__main__":
    app.run(debug=True)


