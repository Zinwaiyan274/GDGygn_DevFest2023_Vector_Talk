import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from pandasai import SmartDataframe
from langchain.llms import OpenAI
import json

app = FastAPI()

# Load data and initialize SmartDataframe
df = pd.read_excel('A.L.I2.xlsx')

# Create a dictionary containing the API token
model_kwargs = {
    "api_key": "KEY"
}
llm = OpenAI(api_key="KEY")

langchain_sdf = SmartDataframe(df, config={"llm": llm})


class Query(BaseModel):
    query: str
    api_key: str


@app.post('/chatbot')
async def main(item: Query):
    if item.api_key != model_kwargs['api_key']:
        return {"error": "Invalid API key"}

    try:
        query = item.query
        langchain_sdf.chat(f" pls output me with pandas dataframe, 0 means there is no [column name], 1 means that Apartments have [column name].... {query}")

        # Access the underlying DataFrame
        converted_df = langchain_sdf.dataframe

        # Convert the DataFrame to JSON
        data = converted_df.Apartments.to_json()
        json_data = json.loads(data)


        return json_data
    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9494)  # Remove the 'debug' argument
