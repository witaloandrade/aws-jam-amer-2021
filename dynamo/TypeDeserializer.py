# https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/types.html
# https://stackoverflow.com/questions/32712675/formatting-dynamodb-data-to-normal-json-in-aws-lambda


from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

def from_dynamodb_to_json(item):
    d = TypeDeserializer()
    return {k: d.deserialize(value=v) for k, v in item.items()}

## Usage:
x = from_dynamodb_to_json({
    "Day": {"S": "Monday"},
    "mylist": {"L": [{"S": "Cookies"}, {"S": "Coffee"}, {"N": "3.14159"}]}
})

y = from_dynamodb_to_json(
    {
                    "CustID": {
                        "S": "task1test1record"
                    },
                    "TnValue": {
                        "N": "250"
                    }
                }
)
# {'Day': 'Monday', 'mylist': ['Cookies', 'Coffee', Decimal('3.14159')]}
print(y)