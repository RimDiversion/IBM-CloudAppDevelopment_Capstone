import requests
import json
import logging
# import related models here
from requests.auth import HTTPBasicAuth
from .models import DealerReview, CarDealer
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

logger = logging.getLogger(__name__)
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url} ")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code} ")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    json_obj = json_payload["review"]
    print(kwargs)
    try:
        response = requests.post(url, json=json_obj, params=kwargs)
    except:
        print("Something went wrong")
    print (response)
    return response
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        if "rows" in json_result["body"]:
            dealers = json_result["body"]["rows"]
            for dealer in dealers:
                content = dealer["doc"]
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=content["address"], city=content["city"], full_name=content["full_name"],
                                   id=content["id"], lat=content["lat"], long=content["long"],
                                   short_name=content["short_name"],
                                   st=content["st"], zip=content["zip"])
                results.append(dealer_obj)
        else:
            dealer = json_result["body"]
            content = dealer["docs"][0]
            dealer_obj = CarDealer(address=content["address"], city=content["city"], full_name=content["full_name"],
                                   id=content["id"], lat=content["lat"], long=content["long"],
                                   short_name=content["short_name"],
                                   st=content["st"], zip=content["zip"])
            results.append(dealer_obj)
        # For each dealer object
        

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    dealerId = kwargs.get("dealerId")
    json_result = get_request(url, dealerId=dealerId)

    if json_result:
        reviews = json_result["body"]["data"]["docs"]

        for review in reviews:
            # sentiment = analyze_review_sentiments(review["review"])
            sentiment = 'positive'
            if review["purchase"] is False:
                review_obj = DealerReview(
                    name = review["name"],
                    purchase = review["purchase"],
                    dealership = review["dealership"],
                    review = review["review"],
                    purchase_date = None,
                    car_make = "",
                    car_model = "",
                    car_year = "",
                    sentiment = sentiment,
                )
                results.append(review_obj)
            else:
                review_obj = DealerReview(
                    name = review["name"],
                    purchase = review["purchase"],
                    dealership = review["dealership"],
                    review = review["review"],
                    purchase_date = review["purchase_date"],
                    car_make = review["car_make"],
                    car_model = review["car_model"],
                    car_year = review["car_year"],
                    sentiment = sentiment,
                )
                results.append(review_obj)
        return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    api_key = "5nUfxXTKn_QgWxBihaKwV7iSflp4rRtLJseP1_IgoUkE"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7605aa17-6907-4f65-80c0-d50429c59c07"
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator)
    nlu.set_service_url(url)

    json_result = nlu.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions()),
        return_analyzed_text = True
    ).get_result()
    sentiment = json_result['sentiment']['document']['label']
    return sentiment


