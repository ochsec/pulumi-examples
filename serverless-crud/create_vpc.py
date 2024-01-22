import pulumi_aws as aws

def create_vpc():
    # Create the VPC for the Aurora serverless DB cluster
    vpc = aws.ec2.Vpc("vpc", cidr_block="10.0.0.0/16")
    azs = aws.get_availability_zones()

    # Create subnets
    subnet1 = aws.ec2.Subnet("subnet1", 
                             vpc_id=vpc.id, 
                             cidr_block="10.0.1.0/24",
                             availability_zone=azs.names[0])
    
    subnet2 = aws.ec2.Subnet("subnet2",
                             vpc_id=vpc.id,
                             cidr_block="10.0.2.0/24",
                             availability_zone=azs.names[1])

    db_subnet_group = aws.rds.SubnetGroup("db_subnet_group",
                                        subnet_ids=[subnet1.id, subnet2.id])

    # security group
    security_group = aws.ec2.SecurityGroup("securityGroup",
                                        vpc_id=vpc.id,
                                        ingress=[{
                                            'protocol': 'tcp',
                                            'from_port': 3306,
                                            'to_port': 3306,
                                            'cidr_blocks': ['0.0.0.0/0'],
                                        }])
    
    return db_subnet_group, security_group