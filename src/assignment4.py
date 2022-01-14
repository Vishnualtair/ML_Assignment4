#Dataset link https://www.kaggle.com/khaiid/most-selling-pc-games
import numpy as np 
import pandas as pd 
import streamlit as st

def dataset_info(game_data):
    #game_data.dropna(inplace = True)
    st.header("Dataset info")
    st.write("Total games : ",game_data[game_data.columns[0]].count())
    st.write("Number of Genres: ",game_data.Genre.drop_duplicates().count())
    st.write("Number of developers: ",game_data.Developer.drop_duplicates().count())
    st.write("Number of Publishers: ",game_data.Publisher.drop_duplicates().count())
    st.write("Total sales made(in millions): ",game_data.Sales.sum())
    return

def make_stmt(str,key):
    default = "The highest no: of games is "
    switch={
        "Genre": default+"developed in "+str+" genre.\n",
        "Developer": default+"developed by "+str+".\n",
        "Publisher": default+"published by "+str+".\n",
    }
    return switch.get(key,"ggez")

def analysis(game_data,ref):
    st.subheader(f"Analysis based on Game {ref}")
    st.bar_chart(data=game_data[ref].value_counts(), width=0, height=0, use_container_width=True) 
    return make_stmt(game_data[ref].value_counts().index[0],ref)

def sales_analyis(game_data):
    st.subheader("Analysis based on Game Sales")
    temp=game_data.groupby(['Name'])['Sales'].sum().nlargest(3)
    st.write("Top 3 games sold : ",temp)
    c_str=(temp.index[0],)

    temp=game_data.groupby(['Genre'])['Sales'].sum().nlargest(3)
    st.write("Top 3 game genre :",temp)
    c_str+=(temp.index[0],)
    
    temp=game_data.groupby(['Publisher'])['Sales'].sum().nlargest(3)
    st.write("Top 3 publishers : ",temp)
    c_str+=(temp.index[0],)
    
    temp=game_data.groupby(['Series'])['Sales'].sum().nlargest(3)
    st.write("Top 3 Series sold : ",temp)
    c_str+=(temp.index[0],)
    st.write("Sales vs Release graph")
    sales = pd.pivot_table(game_data, index = 'Release', values = 'Sales', aggfunc = {'Sales' : np.mean}).sort_values('Sales', ascending = False)
    st.line_chart(data=sales, width=0, height=0, use_container_width=True)
    
    st.info("Note: all sales are in millions.")
    return (f"Most sold game : {c_str[0]}.\nMost sold genre : {c_str[1]}.\nPublisher who sold most : {c_str[2]}.\nMost series sold: {c_str[3]}.")

if __name__=="__main__":
    st.title("Game Sales Analysis")
    data = pd.read_csv('src/Games.csv')
    dataset_info(data)
    conclusion = analysis(data,"Genre")
    conclusion+= analysis(data,"Developer")
    conclusion+= analysis(data,"Publisher")
    conclusion+=sales_analyis(data)
    st.subheader("Summary")
    st.text(conclusion)
 

    