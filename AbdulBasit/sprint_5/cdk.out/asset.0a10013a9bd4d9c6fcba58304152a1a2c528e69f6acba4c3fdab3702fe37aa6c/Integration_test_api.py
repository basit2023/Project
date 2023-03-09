import aws_cdk as core
import aws_cdk.assertions as assertions
import constant as constant
import requests
import boto3 
import json






url=constant.test_url
payload=constant.Payload
payload1=constant.Payload1
#print(payload['S'])
def test_API():
    response=requests.get(url)
    st_code=response.status_code
    assert response.status_code ==200
    if st_code==200:
        print("\n\n\ntest passed\n\n")
test_API()


# def api_put_test():
#     api_test=requests.put(url, data=payload)
    
#     #print("the json value is:",json.loads(api_test.text))
#     if json.loads(api_test.text)==payload:
        
#     #print(api_test.text)
#         print("test pass2")
#         assert True
# api_put_test()
    
# def api_post_test():
#     api_test1=requests.post(url, data=payload1)   #integration test for put operation
#     print("the json value is:",json.loads(api_test1.text))
#     if json.loads(api_test1.text)==payload1:
#          print("test pass")
#          assert True
# api_post_test()











#python3 resource/Integration_test_api.py




