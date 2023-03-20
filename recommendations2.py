import numpy as np
import pandas as pd
import streamlit as st
import joblib
import random
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import datetime as dt
from datetime import date
import matplotlib.pyplot as plot
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted


st.set_page_config(
    page_icon="/Users/Lenovo/Desktop/ISTDSA/DSAG22/proje3/streamlit/CS_logo.png",
    menu_items={
        "Get help": "mailto:juneight79@gmail.com",
        
    }
)

def main():
    st.title("Sales Recommendations App")
    
    menu= ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    
    
    df = pd.read_csv("BankRandomData15thousand.csv")
    df= df.drop(columns=["Unnamed: 0", "age","gender","CityOfBirth","dateOfCustomer","depositAverage"])

    df_new= df.copy()
    df_new.replace("N",0, inplace=True)
    df_new.replace("Y",1, inplace=True)
    df_new["ConsumerLoanOwn"]= df_new["ConsumerLoan"].apply(lambda x: 1 if x>10000 else 0)
    df_new["CarLoanOwn"]= df_new["CarLoan"].apply(lambda x: 1 if x>10000 else 0)
    df_new["MortgageOwn"]= df_new["Mortgage"].apply(lambda x: 1 if x>10000 else 0)
    df_new= df_new.drop(columns=["ConsumerLoan","CarLoan","Mortgage"])
    df_new= df_new.loc[df_new["customer_id"] > 1]
    df_new.reset_index(inplace=True)
    df_new.drop(columns=["index"],inplace=True)

    df_new.values[:,2] = df_new.values[:,2].astype(str)


# Girdi matrisini oluşturma
    matrix = df_new[:10001].values[:,2:]

# Cosine Similarity Matrisini oluşturma
    cos_sim = cosine_similarity(matrix)

    column_name = df_new.columns[1:]
    
    def recom(customer_id):
        for i in range(customer_id-2,customer_id-1):
            similar_index = cos_sim[i].argsort()[int(len(cos_sim[i]) * 0.8)]
            st.write("**Similarities:**")
            st.write("Similarity between Customer **`{}`** and Customer **`{}`** : **`{}`**".format(i+2,similar_index+2,round(cos_sim[i][similar_index],2)))
            st.write("**Products Used by The Customer:**")
            st.markdown(" **`Customer {}`** : **_`{}`_**".format(i+2,','.join(column_name[df_new[:10001].values[i,1:] == 1])))
            st.write("**Products Used by the Similar Customer:**")
            st.markdown(" **`Customer {}`** : **_`{}`_**\n".format(similar_index+2,','.join(column_name[df_new[:10001].values[similar_index,1:] == 1])))
        
        customer_product=np.array((column_name[df_new[:10001].values[i,1:] == 1]))
        similar_customer_product=np.array(column_name[df_new[:10001].values[similar_index,1:] == 1])
        difference = list(set(similar_customer_product) - set(customer_product))
        difference2= list(set(customer_product) - set(similar_customer_product))

        st.write("**Recommendations to the Customer** ")
        st.markdown(":blue[Recommend to customer **`{}`**----> **`{}`** products.]".format(customer_id,','.join(difference))) # my recommendations 
    
    
        if difference ==[] or list(set(customer_product)- set(similar_customer_product))[0:len(list(set(customer_product)- set(similar_customer_product)))] !=[]: 
            st.write("**Recommendations to the Similar Customer** ")
            st.markdown(":red[Recommend to customer **`{}`**----> **`{}`** products.]".format(similar_index+2,','.join(list(set(customer_product)- set(similar_customer_product))[0:len(list(set(customer_product)- set(similar_customer_product)))])))   # alternative recommendations to similar customer
        else:
            pass

    
    


    if choice == "Home":
        st.subheader("What is The Recommendations ?")

                
        with st.form(key="customer_id"):
            customer_id=st.number_input("Please enter customer number and click Submit button.", min_value=2, max_value=10000)
            submit_text = st.form_submit_button(label='Submit')

            st.markdown("""
            <style>
                button.step-up {display: none;}
                button.step-down {display: none;}
                div[data-baseweb] {border-radius: 4px;}
            </style>""",
            unsafe_allow_html=True)

        if submit_text:
                
            st.success("RECOMMENDATION")
            result=recom(customer_id) 
            
            
            st.success("VENN DIAGRAM")
            df = pd.read_csv("BankRandomData15thousand.csv")
            df= df.drop(columns=["Unnamed: 0", "age","gender","CityOfBirth","dateOfCustomer","depositAverage"])

            df_new= df.copy()
            df_new.replace("N",0, inplace=True)
            df_new.replace("Y",1, inplace=True)
            df_new["ConsumerLoanOwn"]= df_new["ConsumerLoan"].apply(lambda x: 1 if x>10000 else 0)
            df_new["CarLoanOwn"]= df_new["CarLoan"].apply(lambda x: 1 if x>10000 else 0)
            df_new["MortgageOwn"]= df_new["Mortgage"].apply(lambda x: 1 if x>10000 else 0)
            df_new= df_new.drop(columns=["ConsumerLoan","CarLoan","Mortgage"])
            df_new= df_new.loc[df_new["customer_id"] > 1]
            df_new.reset_index(inplace=True)
            df_new.drop(columns=["index"],inplace=True)

            

            df_new.values[:,2] = df_new.values[:,2].astype(str)
            matrix = df_new[:10001].values[:,2:]
            cos_sim = cosine_similarity(matrix)
            similar_index = cos_sim[customer_id-2].argsort()[int(len(cos_sim[customer_id-2]) * 0.8)]
            column_name = df_new[:10001].columns[1:]
            CustomerProduct=list(set([','.join(column_name[df_new[:10001].values[customer_id-2,1:] == 1])]))
            SimilarCustomerProduct = list(set([','.join(column_name[df_new[:10001].values[similar_index,1:] == 1])]))
            
            s1=CustomerProduct[0].split(",") 
            s2=SimilarCustomerProduct[0].split(",")
            intersection = set(s1)&set(s2)
            sb=set(s1)-set(s2)
            bs=set(s2)-set(s1)
            fig, ax = plt.subplots(figsize=(17,17))

                   
            v = venn2_unweighted([set(s1), set(s2)], set_labels=('Customer {} Products'.format(customer_id),'SimilarCustomer {} Products'.format(similar_index+2)),alpha=0.5,set_colors=('deepskyblue', 'pink'), ax=ax )
            v.get_label_by_id('10').set_text("{}".format('\n'''.join(list(sb)[0:len(sb)])))
            v.get_label_by_id('01').set_text("{}".format('\n'''.join(list(bs)[0:len(bs)])))
            v.get_label_by_id('11').set_text("{}".format('\n'''.join(list(intersection)[0:len(intersection)])))

            

            
            ax.set_title("Product Ownership", fontsize=16, fontweight='bold',style='italic',bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
            

            
            st.pyplot(fig)

        
   
    else:
        st.subheader("About")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image("/Users/Lenovo/Desktop/ISTDSA/proje5/sunum objeleri/banking.jpg", width=350)
        with col3:
            st.write(' ')

        st.markdown("An application that offers products not used by the customer but used by similar customers as a sales opportunity to the portfolio manager when she logs in by entering the customer number.")
        st.markdown("Due to the confidentiality of bank customer data, the data were generated randomly.")
    
    
        st.image("https://files.realpython.com/media/random_data_watermark.576078a4008d.jpg" , width=300)

        st.dataframe(df[:10001].sample(5, random_state=45))

    
        st.markdown("The products used by the customer from the bank are as follows:")

        st.markdown(         '-' "ConsumerLoan: Credit risk amount")
        st.markdown(         '-' "CarLoan: Credit risk amount")
        st.markdown(         '-' "Mortgage: Credit risk amount")
        st.markdown(         '-' "CreditCard: Y if using the product, N if not")
        st.markdown(         '-' "AddCreditCard: Y if using the product, N if not")
        st.markdown(         '-' "Overdraft: Y if using the product, N if not")   
        st.markdown(         '-' "HGS: Y if using the product, N if not")
        st.markdown(         '-' "DepositAccount: Y if using the product, N if not")
        st.markdown(         '-' "CurrencyDepositAccount: Y if using the product, N if not")
        st.markdown(         '-' "BES: Y if using the product, N if not" )
        st.markdown(         '-' "HouseInsurance: Y if using the product, N if not")
        st.markdown(         '-' "CarInsurance: Y if using the product, N if not")
        st.markdown(         '-' "LifeInsurance: Y if using the product, N if not")
        st.markdown(         '-' "HealthInsurance: Y if using the product, N if not")
        st.markdown(         '-' "ComplementaryHealthInsurance: Y if using the product, N if not")



        

if __name__=='__main__':
    main()


