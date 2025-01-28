from codebase.utilis import *

def inspector(question:str):
    """
    This function checks if the user's question related to database or not.
    args:
        question : the user's question
    returns : True, if the question is related to database, False otherwise.
    """
    try:
        
        #fetching table data
        table = yaml_read(filepath="secrets/tables.yaml", var="tables")

        # prompt
        prompt = yaml_read(var="inspector.prompt")
        #input variables
        input_var = yaml_read(var="inspector.input")

        # setting up llm
        llm = LLM(prompt_temp=prompt,input_var=input_var,output_structure=inspect)

        #invoking the llm
        response = llm.invoke({"table": table,"question": question})
        
        return response.result

    except Exception as e:
        log.error(f"-SUB-MAIN- | action : verifying user's quesiton | inputs : question = {question} | error : {e}")


def sql_query_generator(question : str):
    """
    This function takes question from the user and return a SQL query that will retrieve the answer of that query
    args : 
        question : The question user wants to ask
    returns : SQL query
    """
    try:
        # table details
        table_data = yaml_read(filepath="secrets/tables.yaml", var="tables")
        log.debug(f"-SUB-MAIN- | action : SQL query generation | phase : fetching table details")

        # getting the prompt for the query
        prompt = yaml_read(var="sql_query_generator.prompt")
        log.debug(f"-SUB-MAIN- | action : SQL query generation | phase : fetching the prompt")

        # inputs to the prompt
        input_var = yaml_read(var="sql_query_generator.input")
        log.debug(f"-SUB-MAIN- | action : SQL query generation | phase : fetching the input list")

        # setting LLM for generating the query
        llm = LLM(prompt_temp=str(prompt),input_var=input_var,output_structure=SQL)
        log.debug(f"-SUB-MAIN- | action : SQL query generation | phase : setting up the LLM for the prompt action")
        log.debug(f"-SUB-MAIN- | action : SQL query generation | phase : inoked LLM with inputs | question : {question}")
        # invoke the LLM
        response = llm.invoke({"table_yaml" : table_data, "question": question})
        log.debug(f"-SUB-MAIN- | action : SQL query generation | phase : response generated | question : {question}, response : {response.query}")
        #log.info("action : SQL query generation | phase : finished")
        return response.query
    except Exception as e:
        log.error(f"-SUB-MAIN- | action : SQL query generation | Error : {e}")
        return None

def sql_query_interpreter(question: str, sql_query, sql_response):
    """
    This function answer the question from the sql generated output

    args:
        question : The question asked by the user
        sql_query : the query generated to answer the question
        sql_response : the output from the database using the sql query
    return : answer to the question
    """
    try:
        #log.info("action : SQL query interpretation | phase : started")
        # table data
        table_data = yaml_read(filepath="secrets/tables.yaml", var="tables")
        log.debug(f"-SUB-MAIN- | action : SQL query interpretation | phase : fetching table schema ")

        # prompt
        prompt = yaml_read(var="sql_query_interpreter.prompt")
        log.debug(f"-SUB-MAIN- | action : SQL query interpretation | phase : fetching prompt for sql query interpreation ")

        # input variables
        input_var = yaml_read(var="sql_query_interpreter.input")
        log.debug(f"-SUB-MAIN- | action : SQL query interpretation | phase : fetching input variables of the prompt ")

        # LLM
        llm = LLM(prompt_temp=str(prompt), input_var=input_var)
        log.debug(f"-SUB-MAIN- | action : SQL query interpretation | phase : setting up LLM for the prompt task ")

        # generating the response
        log.debug(f"-SUB-MAIN- | action : SQL query interpretation | phase : invoking the LLM with inputs | question : {question}, sql query : {sql_query} ")
        response = llm.invoke({"table_yaml": table_data, "question": question, "sql_query": sql_query, "sql_output": sql_response})

        log.debug(f"-SUB-MAIN- | action : SQL query interpretation | phase : interpretation generated | response = {response} ")
        #log.info("action : SQL query interpretation | phase : completed\n")
        return response.response
    
    except Exception as e:
        log.error(f"-SUB-MAIN- | action : SQL query interpretation | Error : {e}")
        return None


def fix_sentence(text:str):
    '''
    This function fixes the provided text's grammar.
    '''
    try:
        log.debug(f"-SUB-MAIN- | action : Fixing sentence grammar | user quesiton : {text}" )
        prompt = yaml_read(var="sentence_fix.prompt")
        input_var = yaml_read(var="sentence_fix.input")
        llm = LLM(prompt_temp=prompt,input_var=input_var)
        response = llm.invoke({"text":text})
        return response.response
    except Exception as e:
        log.error(f"-SUB-MAIN- | action : Fixing sentence grammar | error : {e}")
