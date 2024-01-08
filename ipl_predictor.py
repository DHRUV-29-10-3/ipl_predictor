import streamlit as st
import pickle
import pandas as pd
pipe = pickle.load(open('pike.pkl','rb'))
st.title('IPL MATCH PREDICTOR')

teams = ['Delhi Capitals', 'Royal Challengers Bangalore', 'Mumbai Indians',
       'Chennai Super Kings', 'Kolkata Knight Riders', 'Rajasthan Royals',
       'Sunrisers Hyderabad', 'Kings XI Punjab']

cities = ['Mohali', 'Chandigarh', 'Chennai', 'Dharamsala', 'Kolkata',
       'Hyderabad', 'Mumbai', 'Delhi', 'Nagpur', 'Bangalore', 'Durban',
       'Ahmedabad', 'Indore', 'Cuttack', 'Abu Dhabi', 'Jaipur',
       'Visakhapatnam', 'Sharjah', 'Kimberley', 'Cape Town', 'Pune',
       'Port Elizabeth', 'Centurion', 'Bengaluru', 'East London',
       'Raipur', 'Ranchi', 'Johannesburg', 'Bloemfontein']

col1,col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting tem',sorted(teams))
teams2=[]
for team in teams:
    if team == batting_team:
        continue

    else:
        teams2.append(team)

with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams2))


cities = st.selectbox('Select the City',sorted(cities))

target = st.number_input('Target',min_value=0)

col3,col4,col5 = st.columns(3)

with col3 :
    score = st.number_input('Batting Team Score' ,min_value=0)

with col4:
    overs = st.number_input('Overs',min_value=0, max_value=20)

with col5:
    wickets = st.number_input('Wickets Out',min_value=0, max_value=10)

if st.button('Predict Probability'):

    if overs == 0 or target ==0 :
        pass

    elif wickets==10 and score>target:
        st.header("Please enter correct input")

    elif wickets==10 and score<target:
        st.header("Bowling team wins")

    elif overs == 20 and target>score:
        st.header('Bowling team wins')

    elif overs == 20 and target<score:
        st.header('Batting team wins')

    elif score>target:
        st.header("Batting team wins")

    else:
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets = 10 - wickets
        crr = score / overs
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [cities],
                                 'runs_left': [runs_left], 'balls remaining': [balls_left], 'wickets left': [wickets],
                                 'target': [target], 'current run rate': [crr], 'required run rate': [rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + ": " + str(round(win * 100)) + "%")
        st.header(bowling_team + ": " + str(round(loss * 100)) + "%")