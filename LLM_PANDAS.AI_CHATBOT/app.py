from pandasai import SmartDataframe
from langchain.llms import OpenAI
import pandas as pd
from pandasai.llm import OpenAI



df =  pd.read_excel('A.L.I2.xlsx')

llm = OpenAI(api_token="sk-rlIYHdPuagKMf1UVVO8Dr0")
sdf = SmartDataframe(df, config={"llm": llm})

langchain_sdf = SmartDataframe(df, config={"llm": llm})
query = input(str())
print((langchain_sdf.chat(f" pls output me with pandas dataframe, 0 means theere is no [column name]  1 means that Apartments has [columns name].... {query} ")))
