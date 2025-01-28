import os
from langchain_groq import ChatGroq # llm
from langchain_core.prompts import PromptTemplate # for prompt
import yaml # for yaml file read
# for structured output
from typing import Optional
from pydantic import BaseModel, Field

# for sql query execution
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, IntegrityError

# cloud db connection : GCP
from google.cloud.sql.connector import Connector, IPTypes
import aiohttp
import os
from pathlib import Path
# log
from codebase.log import *


'''
------------------------------------
LLM Output structure formats
------------------------------------

'''
# structured output
class Base(BaseModel):
    response : str = Field(description= "The response to the prompt.")
    

class SQL(BaseModel):
    table_name : str = Field(description= "The table name selected from the data.")
    query : str = Field(description= "The sql query to answer the question.")
    message : Optional[str] = Field(default=None, description= "Any explantation or message related to the prompt and its result")

class inspect(BaseModel):
    result : bool = Field(description= "The output after checcking two datas if they are related or not. True, if related, false otherwise. ")



'''
---------------------------
Utility functions
---------------------------
'''


    




# yaml file reader
def yaml_read(var : str, filepath : str = "secrets/config.yaml"):
    """
    This function reads the specified variable from the YAML file.

    Args:
        var: The name of the variable to read.
        filepath: The path to the YAML file.

    Returns:
        The value of the specified variable if found, 
        None otherwise.
    """
    file_path = Path(filepath)
    try:             
        with open(file_path, 'r') as f:
            yaml_data = yaml.safe_load(f)

        def get_yaml_value(data, path):
            """
            Recursively retrieves a value from a nested YAML dictionary.

            Args:
                data: The root YAML dictionary.
                path: A dot-separated string representing the path to the desired value.

            Returns:
                The value at the specified path, or None if the path is invalid.
            """
            if not path:
                return data

            key = path.split(".", 1)[0]
            if key in data:
                remaining_path = path[len(key)+1:] 
                return get_yaml_value(data[key], remaining_path) 
            else:
                return None

        # Replace with the actual filepath
        value = get_yaml_value(yaml_data, var)

        if value:
            return value
        else:
            log.warning(f"--- TOOL -- | action : Reading YAML file | status : Variable not found | variable : {var}")
            exit()
    except FileNotFoundError:
        log.error(f"--- TOOL -- | action : Reading YAML file | status : File not found | path : {filepath} | variable : {var}")
        exit()
        #return None 
        
    except yaml.YAMLError as e:
        log.error(f"--- TOOL -- | action : Reading YAML file | status = Error parsing YAML file | path = {filepath} | variable : {var} | error : {e}")
        exit()
        #return None




def LLM(prompt_temp :str, input_var : list, output_structure : BaseModel = Base):
    """
    This function takes the query and return the response in the provided output_structure format
    
    args :
        output_structure : A pydantic class defining the output structure of the LLM
        prompt : The query of the user
    returns : response in the structured way
    """
    try:
        # prompt    
        prompt = PromptTemplate(input_variables=input_var, template=prompt_temp)
        #dev_log.debug(f"action = LLM input | input prompt = {prompt_temp}, input variables = {input_var}, output structure = {output_structure}")
        # selecting the llm
        model = yaml_read(var="llm_model")
        api_key = str(yaml_read("groq_api_key"))
        llm = ChatGroq(model= model ,api_key = api_key)

        # structured llm
        structured_llm = llm.with_structured_output(output_structure)

        llm_chain = prompt | structured_llm  
        return llm_chain
    except Exception as e:
        log.error(f"--- TOOL -- | action : LLM object | status : Error in creation | error : {e}")
        #return None
        exit()




def query_verify(query: str):
    """
    This function checks if the query has only read code or not. If any write-code is found, it will return False, otherwise True
    args:
        query : The SQL query that would be executed
    returns : True, no write-code is found, False, otherwise
    """
    check_words = ["INSERT","DROP","DELETE","UPDATE", "CREATE"]
    query = query.upper()
    return False if any(word in query for word in check_words) else True



def sql_query_executor(engine, query):
    """
    This function executes the given SQL query using the provided engine

    Args:
        engine: A SQLAlchemy engine object.
        query: The SQL query to be executed.

    Returns:
        A list of tuples representing the query results, 
        or None if an error occurs during execution.
    """

    try:
        with engine.connect() as conn:
            # Use SQLAlchemy's execute() method for better integration           
            result = conn.execute(text(query))
            rows = result.fetchall() 
            return rows 
    except Exception as error:
        log.error(f"--- TOOL -- | action : SQL query execution | query : {query} | Error : {error}")
        #return None
        exit()




# setting up the cloud database connection
# GCP MySQL Server
def setup_clouddb_connection():
    '''
    this funciton sets up conneection to the cloud database and returns an engine object
    '''
    try:
        # default credential path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(yaml_read(var="default_credential_path"))
    except Exception as e:
        log.error(f"--- TOOL -- | CLOUD CONNECTION SET UP | action : setting GOOGLE DEFAULT CREDENTIALS | error : {e}")
        return None
    
    try:
        # getting the variables
        instance_name = str(yaml_read(var="instance_conneciton_name"))
        db_user = yaml_read(var="DB_USER")
        db_pass = yaml_read(var="DB_PASSWORD")
        db_name = yaml_read(var="DB_NAME")
        #db_connection_type = yaml_read(var="IP_Conneciton_type")

        # setting the connection 
        def getconn():
            connector = Connector(ip_type=IPTypes.PUBLIC)
            conn = connector.connect(
            instance_name,
            "pymysql",
            user=str(db_user),
            password=str(db_pass),
            db=str(db_name))
            return conn
    except Exception as e:
        log.error(f"--- TOOL -- | CLOUD CONNECTION SET UP | action : set connection with the Cloud Database with credentials and name | error : {e}")
        return None
    try:
        engine = sqlalchemy.create_engine("mysql+pymysql://", creator=getconn)
        return engine
    except Exception as e:
        log.error(f"--- TOOL -- | CLOUD CONNECTION SET UP | action : creation of engine for the cloud db | error : {e}")
        return None
        
