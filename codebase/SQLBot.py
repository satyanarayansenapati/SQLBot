from codebase.utilis import query_verify, setup_clouddb_connection
from codebase.workflow import *
from codebase.log import *


def SQLBot(question: str): 
      
    try:
        ques = str(fix_sentence(question))
        log.debug(f"MAIN | action : fixing user's question grammartically | updated sentence : {ques}")
        # verifying the question
        response = inspector(question=ques)
        #log.info(f"action : verifying user's question")
        log.debug(f"MAIN | action : verifying user's question ")

        if response:
            
            # query connection
            engine = setup_clouddb_connection()            
           
            # generating query from the qyestion
            sql_query = sql_query_generator(question=ques)
            
            log.debug(f"MAIN | action : SQL query generated | sql query : {sql_query}")
            

            # verifying the sql query
            check_query = query_verify(query=str(sql_query))
            #log.info("action : Checking the query")

            if check_query:
                # execute the query
                sql_output = sql_query_executor(engine=engine,query=sql_query)
                #log.info("action  Executing the query")
                
                # interprete the query
                ans = sql_query_interpreter(question=ques,sql_query=sql_query,sql_response=sql_output)
                log.info("action :  SQL output interpretated and answer delivered\n")
                # return the answer                
                log.debug(f"MAIN | action  SQL query interpreted | answer = {ans}\n")
                return {"question": ques, "answer" : ans}
            else:                
                log.warning(f"action = Query execution denied !!! | question = {ques} | sql query = {sql_query})\n")
                return {"message" : "The question contains command to modify the data. Hence, we cannot proceed!!"}
        else :
            log.warning(f"action : The question isn't related to database | question = {ques}\n")
            return {"message" : "The question can't be answered from database. Please ask questions related to database only. "}
    except Exception as e:        
        log.error(f"MAIN | action : process error | error : {e}\n")
        return {"message" : f"Error occured | Error = {e}"}



