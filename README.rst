============================
Dynamodb Pretty Parser
============================

Parses Dynamodb responses into a more usable format. Results are returned as a list of dictionaries with the attribute names being the key. Results are parsed recursively.
One use is to return results directly to Appsync from a Lambda function.
Parses all scalar types that Dynamo supports

* N (number scalar) - cast as integer or Decimal types
* S (string scalar) - stays string
* SS (string set scalar) - list of strings
* NS (number set scalar) - list of Decimal/integer
* L (list scalar) - list
* BOOL (boolean scalar) - boolean
* B (binary scalar) - string of base64
* BS (binary set scalar) - list of base64 strings
* NULL (null scalar) - None
* M (map scalar) - Dictionary


Responses are returned formated as:

.. code-block:: JSON

  [
    {"attributeOneName": {"S": "value1"}, "attributeTwoName": {"S": "value2"}},
    {"attributeOneName": {"S": "value1"}, "attributeTwoName": {"S": "value2"}}
  ]

Becomes

.. code-block:: JSON

  [
    {"attributeOneName": "value1", "attributeTwoName": "value2"},
    {"attributeOneName": "value1", "attributeTwoName": "value2"}
  ]

Where each dictionary in the top level array is a separate item.

Methods
----------------------------

parseResults(records) -> dict
Arguments:
items -- Response from any boto3 call to Dynamodb that returns Items in the response

Example
----------------------------

.. code-block:: python

  from dynamodbPrettyParser import parseResults
  import boto3

  dynamodb = boto3.client('dynamodb')
  response = dynamodb.query(
    TableName='mytable',
    KeyConditionExpression='my_attribute = :foo',
    ExpressionAttributeValues={':foo': 'bar'}
  )

  print(parseResults(response))
