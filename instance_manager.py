import time
import boto3

ec2 = boto3.client('ec2', region_name='us-east-2')

def launch_instance(instance_type, num_cpus, num_gb_ram):
    response = ec2.run_instances(
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        ImageId="ami-04f167a56786e4b09",
        KeyName="my_key",
        SecurityGroupIds=['sg-046cbb3f577c4a1b7'],
        InstanceInitiatedShutdownBehavior='stop'
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance {instance_id} launched with type {instance_type}")

    ec2.get_waiter('instance_status_ok').wait(InstanceIds=[instance_id])

    return instance_id

def kill_instance(instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"Successfully killed {instance_id}")

instance_id = launch_instance('t2.micro', 1, 1)
time.sleep(5)
terminate_instance(instance_id)

