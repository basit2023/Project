import aws_cdk as core
import aws_cdk.assertions as assertions
import constant as constant
import requests
import boto3 
import json






url=constant.test_url
payload=constant.Payload
#print(payload['S'])
def test_API():
    response=requests.get(url)
    st_code=response.status_code
    assert response.status_code ==200
    if st_code==200:
        print("\n\n\ntest passed\n\n")
test_API()


# def api_put_test():
#     api_test=requests.put(url, params=payload)
#     print("the json value is:",json.loads(api_test.text))
#     if json.loads(api_test.text)==payload:
         
#     #print(api_test.text)
#          print("test pass")
#          assert True
# api_put_test()
    











#python3 resource/Integration_test_api.py




