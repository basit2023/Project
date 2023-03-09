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


def api_put_test():
    api_test=requests.put(url, data=payload)
    st_code=api_test.status_code
    assert api_test.status_code ==200
    if st_code==200:
        print("\n\n\ntest passed")
        print(json.loads(api_test.text),"\n\n")
        
   
    
api_put_test()
    
def api_post_test():
    api_test_delete=requests.delete(url, data=payload1)   #integration test for put operation
    
    st_code=api_test_delete.status_code
    assert api_test_delete.status_code ==200
    if st_code==200:
        print("\n\n\ntest passed")
        print(json.loads(api_test_delete.text),"\n\n")

    #      assert True
api_post_test()











#python3 resource/Integration_test_api.py




