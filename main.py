from fastapi import FastAPI, status
from codebase.SQLBot import SQLBot
from codebase.log import *

# creating an instance
app = FastAPI()

# funciton
@app.get("/sqlbot")
async def sqlbot(question: str):
    try:
        log.info("Question Received")
        # Use SQLBot to process the question and get the response
        response = await SQLBot.process_question(question)  # Assuming asynchronous processing
        log.info("Answer delivered" )
        if response.answer is None:
            return {"status" : status.HTTP_204_NO_CONTENT, "Answer" : "ERROR !! Please contanct customer support"}
        return {"status" : status.HTTP_200_OK, "Answer" : response} 
 
    except Exception as e:
        log.error(f"SERVER | Error: {e}\n\n\n")  # Log the error using the logger object
        return {"status" : status.HTTP_500_INTERNAL_SERVER_ERROR, "Error" : e}  # Return an error response with status code 500
    

@app.get("/")
def home():
    return "This is SQLBot API"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 



