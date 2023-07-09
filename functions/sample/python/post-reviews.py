from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core import ApiException


def formResponse(statusCode, body):
    return {
        "statusCode": statusCode,
        "headers": {"Content-Type": "application/json"},
        "body": body
    }


def main(dict):
    secret = {
        "COUCH_URL":
        "https://53d3b9cc-ddd5-48db-9647-ea8d66f2ccd3-bluemix.cloudantnosqldb.appdomain.cloud",
        "COUCH_USERNAME": "53d3b9cc-ddd5-48db-9647-ea8d66f2ccd3-bluemix",
        "IAM_API_KEY": "nqgg3f0cV0dmeNiTcGdqNbF2rg1jSE9-2LfK1qXgf05k"
    }

    authenticator = IAMAuthenticator(
        secret["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret["COUCH_URL"])

    try:
        posted_review = Document(
            review_id=dict["review"]["review_id"],
            name=dict["review"]["name"],
            dealership=dict["review"]["dealership"],
            review=dict["review"]["review"],
            purchase=dict["review"]["purchase"],
            purchase_date=dict["review"]["purchase_date"],
            car_make=dict["review"]["car_make"],
            car_model=dict["review"]["car_model"],
            car_year=dict["review"]["car_year"]
        )
        uuid = service.get_uuids(count=1).get_result()
        thisUuid = uuid["uuids"][0]
        response = service.put_document(
            db="reviews",
            doc_id=thisUuid,
            document=posted_review).get_result()
        return formResponse(200, response)
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
        return formResponse(int(ae.code), errorBody)
    except:
        return formResponse(500, {"error": "Something went wrong on the server"})


main({"review": {"review_id": 1115, "name": "Upkar Lidder", "dealership": 15, "review": "Great service!", "purchase": False,
                 "another": "field", "purchase_date": "02/16/2021", "car_make": "Audi", "car_model": "Car", "car_year": 2021}})