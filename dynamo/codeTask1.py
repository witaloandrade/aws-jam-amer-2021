#!/usr/bin/env python3
import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

def dynamodb_deserializer_to_json(item):
  #### ADD CODE FOR DESERIALIZER ####
  d_item = TypeDeserializer()
  return {k: d_item.deserialize(value=v) for k, v in item.items()}
  
def get_item_cust_profile(dynamo_table, cust_id):
  #### ADD CODE TO QUERY TABLE ####
  #results = "YOUR CODE GOES HERE"
  #return cust_profile
  response = dynamo_table.get_item(
    Key={
        'CustID': cust_id
    }
  )
  print('LOG RESPONSE IS ', response['Item'])
  print('LOG CustID IS ', response['Item']['CustID'])
  return  response['Item']


def put_item_cust_profile_table(dynamo_table, cust_profile):
  #### ADD CODE TO UPDATE TABLE ####
  #response = "YOUR CODE GOES HERE"
  #return response
  response = dynamo_table.put_item(
   Item=cust_profile
  )
  return response


def handler(event, context):
  region = os.environ['AWS_REGION']
  records = event["Records"]

  dynamodb = boto3.resource('dynamodb', region_name=region)
  dynamo_table = dynamodb.Table('CustProfile')

  for record in records:
    if record["eventName"] == "INSERT":
      
      item = dynamodb_deserializer_to_json(record["dynamodb"]["Keys"])
      # CustID 	string 	Unique identifier for customer
      cust_profile = get_item_cust_profile(dynamo_table, item["CustID"])                
      # Check if customer exist in table
      print('LOG cust_profile IS ', cust_profile)
      if cust_profile:
        profile = cust_profile
        profile["TotalTnValue"] = int(profile["TotalTnValue"]) + int(item["TnValue"])
        print('LOG TotalTnValue IS ', profile["TotalTnValue"])
      else:
        profile = dict()
        profile["CustID"] = item["CustID"]
        profile["TotalTnValue"] = item["TnValue"]

      if profile["TotalTnValue"] < 1000:
        cust_status = "Normal"
      else:
        cust_status = "Elite"

      profile["CustStatus"] = cust_status
      print('LOG profile IS ', profile)
      response = put_item_cust_profile_table(dynamo_table, profile)
      print('LOG RESPONSE IS ', response)
        
  return {
      'statusCode': 200,
      'body': json.dumps("Success")
  }
