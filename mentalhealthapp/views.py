from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Bookings, Users
import pandas as pd
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# Create your views here.
def index(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=Users.objects.get(email=current_user)
        return render(request,"index.html",{'current_user':current_user,'user':user})
    return render(request,"index.html")
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        passw=request.POST['password']
        confirmpass=request.POST['confirmpassword']
        ph=request.POST['phonenumber']
        gender=request.POST['gender']
        age=request.POST['age']
        place=request.POST['place']
        emailexist=Users.objects.filter(email=email)
        if emailexist:
            messages.error(request,"emailID already registered")
        elif passw!=confirmpass:
            messages.error(request,"password does not match")
        else:
             Users.objects.create(name=name,email=email,createpassword=passw,Phonenumber=ph,age=age,gender=gender,place=place)
             return redirect('/')
    return render(request,"register.html")
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        passw=request.POST['password']
        user=Users.objects.filter(email=email,createpassword=passw)
        if user:
            request.session['email']=email
            return redirect('/')    
        else:
            messages.error(request,"User name and password doesnot match")
    return render(request,"login.html")
def logout(request):
    del request.session['email']
    return redirect('/')
def myprofile(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=Users.objects.get(email=current_user)
        return render(request,"profile.html",{'user':user})
def updateprofile(request,id):
    user=Users.objects.get(id=id)
    if request.method=='POST':
        name=request.POST['name']
        passw=request.POST['password']
        confirmpass=request.POST['confirmpassword']
        ph=request.POST['phonenumber']
        gender=request.POST['gender']
        age=request.POST['age']
        place=request.POST['place']
        if passw!=confirmpass:
            messages.error(request,"password does not match")
        else:
            user.name=name
            user.createpassword=passw
            user.Phonenumber=ph
            user.gender=gender
            user.age=age
            user.place=place
            user.save()
            return redirect('profile')
    return render(request,"updateprofile.html",{'user':user})
def prediction(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=Users.objects.get(email=current_user)
        if request.method=='POST':
            # Load dataset
            dataset = pd.read_csv("static/csv/health.csv")
            dataset.drop(columns=['Quarantine_Frustrations'], inplace=True)
            # Define encoding mappings
            encoding_mappings = {
                'Age': {'16-20': 0, '20-25': 1, '25-30': 2, '30-Above': 3},
                'Gender': {'Male': 0, 'Female': 1},
                'Occupation': {'Corporate': 0, 'Others': 1, 'Student': 2, 'Housewife': 3, 'Business': 4},
                'Days_Indoors': {'1-14 days': 0, '15-30 days': 1, '31-60 days': 2, 'More than 2 months': 3, 'Go out Every day': 4},
                'Growing_Stress': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Changes_Habits': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Mental_Health_History': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Weight_Change': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Mood_Swings': {'Low': 0, 'Medium': 1, 'High': 2},
                'Coping_Struggles': {'No': 0, 'Yes': 1},
                'Work_Interest': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Social_Weakness': {'No': 0, 'Maybe': 1, 'Yes': 2}
            }
            # Label encoding
            label_encoders = {}
            for column, mapping in encoding_mappings.items():
                le = LabelEncoder()
                dataset[column] = le.fit_transform(dataset[column])
                label_encoders[column] = le
        
            # Random Forest Model
            x = dataset.drop('Coping_Struggles', axis=1).values
            y = dataset['Coping_Struggles'].values
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

            randomforest = RandomForestClassifier(n_estimators=100, criterion="entropy", random_state=42)
            randomforest.fit(x_train, y_train)

            # Predictions
            y_pred_train = randomforest.predict(x_train)
            y_pred_test = randomforest.predict(x_test)
            # Define encoding mappings
            encoding_mappings = {
                'Age': {'16-20': 0, '20-25': 1, '25-30': 2, '30-Above': 3},
                'Gender': {'Male': 0, 'Female': 1},
                'Occupation': {'Corporate': 0, 'Others': 1, 'Student': 2, 'Housewife': 3, 'Business': 4},
                'Days_Indoors': {'1-14 days': 0, '15-30 days': 1, '31-60 days': 2, 'More than 2 months': 3, 'Go out Every day': 4},
                'Growing_Stress': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Changes_Habits': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Mental_Health_History': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Weight_Change': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Mood_Swings': {'Low': 0, 'Medium': 1, 'High': 2},
                'Coping_Struggles': {'No': 0, 'Yes': 1},
                'Work_Interest': {'No': 0, 'Maybe': 1, 'Yes': 2},
                'Social_Weakness': {'No': 0, 'Maybe': 1, 'Yes': 2}
            }

            # Assuming 'x' and 'y' are already defined

            # Split the dataset into train and test sets
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

            # Train the Random Forest model
            randomforest = RandomForestClassifier(n_estimators=100, criterion="entropy", random_state=42)
            randomforest.fit(x_train, y_train)

            # Predictions
            y_pred_train = randomforest.predict(x_train)
            y_pred_test = randomforest.predict(x_test)
            # Take input features from the user
            print("Please provide the following information:")
            sex = request.POST['gender']
            age = int(request.POST['age'])
            occupation = request.POST['occupation']
            days_indoors = request.POST['indoordays']
            growing_stress = request.POST['stress']
            changes_habits = request.POST['habits']
            mental_health_history = request.POST['mentalhealth']
            weight_change = request.POST['weight']
            mood_swings = request.POST['moodswing']
            work_interest = request.POST['work']
            social_weakness = request.POST['weakness']

            # Preprocess user input
            input_data = [[sex, age, occupation, days_indoors, growing_stress, changes_habits,
               mental_health_history, weight_change, mood_swings, work_interest,
               social_weakness]]

            # Make prediction
            prediction = randomforest.predict(input_data)

            # Print prediction
            if prediction == 0:
                messages.success(request," is not struggling with mental health.")
                messages.success(request," dont want to consult any doctor")
                return render(request,"healthprediction.html",{'user':user,'result':prediction})
            else:
                messages.success(request," is struggling with mental health.")
                messages.success(request," have to consult a doctor")
                return render(request,"healthprediction.html",{'user':user,'result':prediction})
        return render(request,"healthprediction.html",{'user':user})
    return render(request,"healthprediction.html")
def doctors(request):
    return render(request,"doctors.html")
def booking(request,doctor):
    if 'email' in request.session:
        current_user=request.session['email']
        user=Users.objects.get(email=current_user)
        dname=doctor
        if request.method=='POST':
            email=request.POST['email']
            doctor=request.POST['dname']
            amount=request.POST['bookingfee']
            cardno=request.POST['cardnumber']
            edate=request.POST['edate']
            cvv=request.POST['cvv']
            Bookings.objects.create(Name=email,Doctor=doctor,Price=amount,Cardno=cardno,Edate=edate,Cvv=cvv)
            return redirect('/')    
        return render(request,"paymentform.html",{'user':user,'doctor':dname})
    return render(request,"paymentform.html")
def precuations(request):
    return render(request,"precuations.html")
def paymenthistory(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=Users.objects.get(email=current_user)
        data=Bookings.objects.filter(Name=user.email)
        return render(request,"paymenthistory.html",{'user':user.name,'data':data})