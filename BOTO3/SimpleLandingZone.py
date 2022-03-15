import boto3

ec2 = boto3.resource('ec2')

# 1. create VPC
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc.create_tags(Tags=[
  {"Key": "Name", "Value": "vpc-yeonkyu-02"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
vpc.wait_until_available()
print(vpc.id)

# 2. create then attach internet gateway
ig = ec2.create_internet_gateway()
ig.create_tags(Tags=[
  {"Key": "Name", "Value": "ig-yeonkyu-02"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

# 3. create public route table and private route table
public_route_table = vpc.create_route_table()
public_route_table.create_tags(Tags=[
  {"Key": "Name", "Value": "rt-public-yeonkyu-02"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
publicRoute = public_route_table.create_route(
  DestinationCidrBlock='0.0.0.0/0',
  GatewayId=ig.id
)

private_route_table = vpc.create_route_table()
private_route_table.create_tags(Tags=[
  {"Key": "Name", "Value": "rt-private-yeonkyu-02"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])

try:
  privateRoute = public_route_table.create_route()
except Exception as e:
  print(e)


# 4. create subnet
public_subnet_01 = ec2.create_subnet(
  CidrBlock='10.0.1.0/24', VpcId=vpc.id
)
public_subnet_01.create_tags(Tags=[
  {"Key": "Name", "Value": "public-subnet-yeonkyu-021"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
public_subnet_02 = ec2.create_subnet(
  CidrBlock='10.0.2.0/24', VpcId=vpc.id
)
public_subnet_02.create_tags(Tags=[
  {"Key": "Name", "Value": "public-subnet-yeonkyu-022"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
private_subnet_01 = ec2.create_subnet(
  CidrBlock='10.0.3.0/24', VpcId=vpc.id
)
private_subnet_01.create_tags(Tags=[
  {"Key": "Name", "Value": "private-subnet-yeonkyu-021"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
private_subnet_02 = ec2.create_subnet(
  CidrBlock='10.0.4.0/24', VpcId=vpc.id
)
private_subnet_02.create_tags(Tags=[
  {"Key": "Name", "Value": "private-subnet-yeonkyu-022"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])

# associate the route table with the subnet
public_route_table.associate_with_subnet(SubnetId=public_subnet_01.id)
public_route_table.associate_with_subnet(SubnetId=public_subnet_02.id)
private_route_table.associate_with_subnet(SubnetId=private_subnet_01.id)
private_route_table.associate_with_subnet(SubnetId=private_subnet_02.id)


# Create sec group
sec_group = ec2.create_security_group(
  GroupName='sec_yeonkyu_1', Description='Sec Group for Public', VpcId=vpc.id
)
sec_group.authorize_ingress(
  IpPermissions=[
    {
      "FromPort": 22,
      "ToPort": 22,
      "IpProtocol": "tcp",
      "IpRanges": [
        {"CidrIp": "0.0.0.0/0", "Description": "internet"},
      ],
    },
    {
      "FromPort": 80,
      "ToPort": 80,
      "IpProtocol": "tcp",
      "IpRanges": [
        {"CidrIp": "0.0.0.0/0", "Description": "internet"},
      ],
    },
  ],
)
sec_group.create_tags(Tags=[
  {"Key": "Name", "Value": "sec-yeonkyu-2"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])

# Create instance
instances = ec2.create_instances(
  ImageId='ami-04204a8960917fd92', InstanceType='t2.micro', MaxCount=1, MinCount=1, KeyName='yeonkyu-keypair',
  NetworkInterfaces=[
    {
      'SubnetId': public_subnet_01.id,
      'DeviceIndex': 0,
      'AssociatePublicIpAddress': True,
      'Groups' : [sec_group.group_id]
    }
  ]
)
instances[0].create_tags(Tags=[
  {"Key": "Name", "Value": "ec2-yeonkyu-2"},
  {"Key": "User", "Value": "yeonkyu@lgcns.com"}
])
instances[0].wait_until_running()
print(instances[0].id)












