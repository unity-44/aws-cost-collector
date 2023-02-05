import boto3
import datetime

# specify aws-cli profile e.g. default
aws_profile = input("Please enter your AWS Profile: ")
boto3.setup_default_session(profile_name=aws_profile)

def ec2_get_running_instances(client):
    # get a list of all running EC2 instances
    instances = client.describe_instances(Filters=[{
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        }])

    ec2_running_instances = []
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            ec2_running_instances.append(instance)

    return ec2_running_instances


def rds_get_running_instances(client):
    # get a list of all running RDS instances
    rds_instances = client.describe_db_instances()

    rds_running_instances = []

    for instance in rds_instances["DBInstances"]:
        rds_running_instances.append(instance)

    return rds_running_instances


def ec2_calculate_cost(instances):
    # calculate cost of EC2 instance (fixed price) / manual input or price lookup by InstanceType in next version
    ec2_cost_dict = {}

    for instance in instances:
        launch_time = instance["LaunchTime"]
        current_time = datetime.datetime.now(datetime.timezone.utc)
        running_time = current_time - launch_time
        running_time = running_time.total_seconds() / 3600
        cost = round(running_time * 0.12, 2)

        ec2_cost_dict[instance["InstanceId"]] = cost
        
    return ec2_cost_dict


def rds_calculate_cost(instances):
    # calculate cost of RDS instance (fixed price) / manual input or price lookup by InstanceType in next version
    rds_cost_dict = {}

    for instance in instances:
        create_date = instance["InstanceCreateTime"]
        current_time = datetime.datetime.now(datetime.timezone.utc)
        running_time = current_time - create_date
        running_time = running_time.total_seconds() / 3600
        cost = round(running_time * 0.12, 2)
        
        rds_cost_dict[instance["DBInstanceIdentifier"]] = cost
        return rds_cost_dict
    

def send_sns_notification(client, ec2, rds):
    # send e-mail via sns to topic
    message = f"You have instances running that are over 1€. Here is your overview \n EC2: {ec2} \n RDS: {rds}"

    client.publish(
        TargetArn="arn:aws:sns:eu-central-1:140212857939:instances",
        Message=message,    
    )

def check_expensive_instances(dict):
    # check for instances (EC2 and RDS) that are over 1€ -> expensive. Manual expensive input in next version
    instance_dict = {}

    for key, value in dict.items():
        if value >= 1:
            instance_dict[key] = value

    return instance_dict

def create_history(ec2_instances, rds_instances):
    combined_dict = {**ec2_instances, **rds_instances}

    file = open("history.csv", "a")
    file.write((str(datetime.datetime.now()) + " " + str(combined_dict)) + " \n" )

def main():
    # call functions and send sns notification
    ec2 = boto3.client("ec2")
    rds = boto3.client("rds")
    sns = boto3.client("sns")

    ec2_instances = ec2_get_running_instances(ec2)
    rds_instances = rds_get_running_instances(rds)

    ec2_cost = ec2_calculate_cost(ec2_instances)
    rds_cost = rds_calculate_cost(rds_instances)

    ec2_expensive = check_expensive_instances(ec2_cost)
    rds_expensive = check_expensive_instances(rds_cost)

    print("You have expensive EC2 Instances: " + str(ec2_expensive))
    print("You have expensive RDS Instances: " + str(rds_expensive))

    send_sns_notification(sns, ec2_expensive, rds_expensive)
    

    print(ec2_cost)
    print(rds_cost)

    create_history(ec2_cost, rds_cost)


main()