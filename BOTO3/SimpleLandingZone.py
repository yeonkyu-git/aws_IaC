import boto3

ec2 = boto3.resource('ec2')

# 1. VPC 생성
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc.create_tags(Tags=[
  {"Key": "Name", "Value": "vpc-yeonkyu-02"}
])
vpc.wait_until_available()
print(vpc.id)

# 2. 인터넷 게이트웨이 생성 후 VPC에 Attach
ig = ec2.create_internet_gateway()
ig.create_tags(Tags=[
  {"Key": "Name", "Value": "ig-yeonkyu-02"}
])
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)

# 3. 퍼블릭 라우팅 테이블, 프라이빗 라우팅 테이블 생성
public_route_table = vpc.create_route_table()
public_route_table.create_tags(Tags=[
  {"Key": "Name", "Value": "rt-public-yeonkyu-02"}
])
publicRoute = public_route_table.create_route(
  DestinationCidrBlock='0.0.0.0/0',
  GatewayId=ig.id
)

private_route_table = vpc.create_route_table()
private_route_table.create_tags(Tags=[
  {"Key": "Name", "Value": "rt-private-yeonkyu-02"}
])

try:
  privateRoute = public_route_table.create_route()
except Exception as e:
  print(e)


# 4. 서브넷 생성 (퍼블릭 2개, 프라이빗 2개)
public_subnet_01 = ec2.create_subnet(
  CidrBlock='10.0.1.0/24', VpcId=vpc.id
)
public_subnet_01.create_tags(Tags=[
  {"Key": "Name", "Value": "public-subnet-yeonkyu-021"},
])
public_subnet_02 = ec2.create_subnet(
  CidrBlock='10.0.2.0/24', VpcId=vpc.id
)
public_subnet_02.create_tags(Tags=[
  {"Key": "Name", "Value": "public-subnet-yeonkyu-022"}
])
private_subnet_01 = ec2.create_subnet(
  CidrBlock='10.0.3.0/24', VpcId=vpc.id
)
private_subnet_01.create_tags(Tags=[
  {"Key": "Name", "Value": "private-subnet-yeonkyu-021"}
])
private_subnet_02 = ec2.create_subnet(
  CidrBlock='10.0.4.0/24', VpcId=vpc.id
)
private_subnet_02.create_tags(Tags=[
  {"Key": "Name", "Value": "private-subnet-yeonkyu-022"}
])

# associate the route table with the subnet
public_route_table.associate_with_subnet(SubnetId=public_subnet_01.id)
public_route_table.associate_with_subnet(SubnetId=public_subnet_02.id)
private_route_table.associate_with_subnet(SubnetId=private_subnet_01.id)
private_route_table.associate_with_subnet(SubnetId=private_subnet_02.id)


# 보안그룹 생성
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
  {"Key": "Name", "Value": "sec-yeonkyu-2"}
])

# EC2 인스턴스 생성
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
  {"Key": "Name", "Value": "ec2-yeonkyu-2"}
])
instances[0].wait_until_running()
print(instances[0].id)












