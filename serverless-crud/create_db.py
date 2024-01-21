import os
import pulumi_aws as aws
from dotenv import load_dotenv

# Load env
load_dotenv()

def create_db(db_subnet_group, security_group):

    db_cluster = aws.rds.Cluster("dbCluster",
                                engine=aws.rds.EngineType.AURORA_MYSQL,
                                engine_mode="serverless",
                                db_subnet_group_name=db_subnet_group.name,
                                vpc_security_group_ids=[security_group.id],
                                master_username=os.getenv("MASTER_USERNAME"),
                                master_password=os.getenv("MASTER_PASSWORD"),
                                skip_final_snapshot=True)
    
    return db_cluster
