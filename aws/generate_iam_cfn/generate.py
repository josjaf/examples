import re

api_calls = """accept_reserved_instances_exchange_quote()
accept_vpc_endpoint_connections()
accept_vpc_peering_connection()
allocate_address()"""


for line in api_calls.splitlines():
    removed_underscores = re.sub(r"[()]", "", line)
    word_list = removed_underscores.split("_")
    final = ''
    for word in word_list:
        final = final + word.capitalize()
    final = '- ec2:' + final     
    print(final)


# copy and paste from the client section
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#client
