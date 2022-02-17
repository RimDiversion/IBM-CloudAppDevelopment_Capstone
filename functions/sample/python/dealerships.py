import sys 
from cloudant.client import Cloudant
from cloudant.error import CloudantException

def main(dict): 

    secret= { 
        "COUCH_URL": "https://10576f8c-29b4-4de5-890d-2c10096bf97c-bluemix.cloudantnosqldb.appdomain.cloud", 
        "IAM_API_KEY": "7f1h3WqmR2tUHoCt0sD-jo1ZxRvXVn585J7xVh2VB-R0", 
        "COUCH_USERNAME": "10576f8c-29b4-4de5-890d-2c10096bf97c-bluemix" 
        } 

    client =Cloudant.iam(
        account_name=secret["COUCH_URL"], 
        api_key=secret["IAM_API_KEY"],
        connect=True, 
        )
        
    my_database= client["reviews"]    

    try: 
        selector = {'id': {'$eq': int(dict["id"])}} 
        result_by_filter=my_database.get_query_result(selector,raw_result=True) 
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':result_by_filter} 
            }        
        return result 

    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }