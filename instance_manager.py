import time
import boto3
import shlex

ec2 = boto3.client('ec2', region_name='us-east-2')
ssm = boto3.client('ssm', region_name='us-east-2')

IAM_ROLE_NAME = "CherryPickRole"

def launch_instance(instance_type, num_cpus, num_gb_ram, name="Cherrypick-Instance"):
    response = ec2.run_instances(
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        ImageId="ami-04f167a56786e4b09",
        KeyName="my_key",
        SecurityGroupIds=['sg-046cbb3f577c4a1b7'],
        InstanceInitiatedShutdownBehavior='stop',
        IamInstanceProfile={'Name': IAM_ROLE_NAME},
        UserData=f'#!/bin/bash\npython3 test.py',
    )

    instance = response['Instances'][0]
    instance_id = instance['InstanceId']

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': name}]
    )
    print(f"Instance {instance_id} launched with type {instance_type}")
    print("Initializing...")

    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    ec2.get_waiter('instance_status_ok').wait(InstanceIds=[instance_id])

    print("Initialization Complete!")

    return instance_id

def kill_instance(instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"Successfully killed {instance_id}")

def read_script_from_file(file_name):
    with open(file_name, "r") as f:
        script_content = f.read()
    return script_content

def run_script_via_ssm(instance_id, file_name):
    script = f"#!/bin/bash\n python3 -c {shlex.quote(read_script_from_file(file_name))}"

    print(f"Running {file_name} on instance {instance_id}")
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [script]}
    )
    print("Command Sent!")

    command_id = response['Command']['CommandId']

    time.sleep(2)
    output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
    while True:
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
        if output['Status'] in ['Success', 'Failed']:
            break
        print("Waiting for script...")
        time.sleep(2)

    print("Command Output")
    print(output['StandardOutputContent'])
    print("Command Error output")
    print(output['StandardErrorContent'])
    print("Command Status: ", output['Status'])

instance_id = launch_instance('t2.micro', 1, 1)
try:
    run_script_via_ssm(instance_id, "test.py")
except Exception as e: 
    print("Script Failed!!")
    print(e)

kill_instance(instance_id)
                        
