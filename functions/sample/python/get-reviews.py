from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
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
        selector = {"dealership": {"$eq": int(dict["dealerId"])}}
        response = service.post_find(
            db="reviews",
            selector=selector
        ).get_result()
        if (len(response["docs"]) == 0):
            return formResponse(404, response)
        else:
            return formResponse(200, response)
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
        return formResponse(int(ae.code), errorBody)
    except:
        return formResponse(500, {"error": "Something went wrong on the server"})


main({"dealerId": 15})