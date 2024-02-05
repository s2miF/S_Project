
import numpy as np
import pandas as pd 
import pickle as pi
import streamlit as st
from sklearn.preprocessing import LabelEncoder


lm = pi.load(open('dtr_pkl', 'rb'))

st.markdown('<style>body{background-color: red;}</style>',unsafe_allow_html=True)

primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"
st.title("عدد السكان في المملكة العربية السعودية")



def predict (input_data):
  
    le=LabelEncoder()
    inp = le.fit_transform(input_data)
    input_as_np = np.array(inp).reshape(-1,4)
    pre = lm.predict(input_as_np)
    pr = pre.astype(int)
    return(f"العدد المتوقع : {pr}")




def main():
    

    region = st.selectbox("المدينة ",
                     ("Al Bahah","Al Jawf",
                      "Al Madinah Al Munawwarah", "Al Qaseem",
                      "Ar Riyadh","Aseer",
                      "Eastern Region","Hail","Jazan",
                      "Makkah Al Mukarramah","Najran",
                      "Northern Borders","Tabuk"))
    nationality = st.selectbox("الجنسية",("Saudi", "Non-Saudi"))

    year = st.number_input("السنة", min_value=2023, max_value=2030,
                 help="ضع السنة التي تريد توقع عدد السكان حينها")
    gender = st.selectbox("الجنس",("Female", "Male"))
#option = st.selectbox("charts",("line", "bar"))

    st.subheader(f"عدد السكان المتوقع عام {year}")
    
    dignosis = ''
    # creating a button for perdiction
    if st.button('Result'):
        dignosis = predict([gender,nationality,region,year])

        
    st.success(dignosis)
    
if __name__=='__main__':
    main()

