import boto3
cw = boto3.client('cloudwatch')
response = cw.set_alarm_state(
    AlarmName='BillingAlarm-Terraform',
    StateValue='OK',
    StateReason='Test',
)
print(response)