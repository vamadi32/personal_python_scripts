import boto
def lambda_handler(event, context):
    
    # Connect to the Amazon EC2 service
    ec2 = boto3.resource('ec2')

    # Loop through each instance
    for instance in ec2.instances.all():
      state = instance.state['Name']
      for tag in instance.tags:


        # Check for the 'startstopinator' tag
        if tag['Key'] == 'start-stopinator' or tag['Key'] == 'stop-stopinator':

          action = tag['Value'].lower()

          # Stop if instance is running
          if action == 'stop' and state == 'running':
            print ("Stopping instance", instance.id)
            instance.stop()

          # Start instance if instance is stopped
          elif action == 'start' and state == 'stopped':
            print ("Starting instance", instance.id)
            instance.terminate()