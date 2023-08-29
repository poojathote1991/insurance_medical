import config
import pymongo

mongo_client=pymongo.MongoClient(f'mongodb://localhost:{config.MOGODB_PORT_NUMBER}')
db=mongo_client[config.MONGODB_DB_NAME]
collection_user=db['user_details']
collection_pred=db['model_prediction']


def save_regestration_details(name,emailid,mobileno,passward):
    
    response=collection_user.find_one({
                               "Email Id ":emailid,
                              })
    if response:
        return "Email id alread exists"
    
    response=collection_user.find_one({"Mobile No": mobileno})

    if response:
        return "Mobile number alread exists"
    
    response=collection_user.insert_one({"Name ":name,
                                "Email Id ":emailid,
                                "Mobile No":mobileno,
                                "Passward":passward})
    
    return "user registerd successfully"

def login_user(emailid,passward):
    response=collection_user.find_one({"Email Id ": emailid})
    if not response:
        return "user not exists"

    response=collection_user.find_one({"Email Id ": emailid,
                              "Passward ":passward})
    print(response)

    if response:
        return "user login sucessfully"
    
    else:
        return "user enter incorrect email or passward"

def save_predicted_data(age,gender,bmi,children,smoker,region,pred_price):
    response=collection_pred.insert_one({"Age":age,
                                         "Gender":gender,
                                         "BMI":bmi,
                                         "Children":children,
                                         "Smoker":smoker,
                                         "Region":region,
                                         "Pred_price":pred_price})
    