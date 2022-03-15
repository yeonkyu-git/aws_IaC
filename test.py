import boto3

ec2 = boto3.resource('ec2')
vpc = ec2.Vpc('vpc-09db377a4851114ab')
subnet = ec2.Subnet('subnet-0a539efd9b987e1d0')

instances = ec2.create_instances(
  ImageId='ami-04204a8960917fd92',
  MinCount=1,
  MaxCount=1,
  InstanceType='t2.micro',
  KeyName='yeonkyu-keypair',
  SubnetId='subnet-0a539efd9b987e1d0'
)