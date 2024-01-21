import pulumi

from create_vpc import create_vpc
from create_db import create_db

# Create 2 subnets and a security group for port 3306
db_subnet_group, security_group = create_vpc()

# Create the Aurora serverless cluster and export the dbCluster, cluster_id
db_cluster = create_db(db_subnet_group, security_group)

pulumi.export("cluster_endpoint", db_cluster.endpoint)
pulumi.export("cluster_id", db_cluster.id)
