import aws

cmd = aws.awscmd()
#creating key-pair
keyname = input("Enter Key-name: ")
cmd.key_pair(keyname)

#creating security group
sg_name = input("Enter Security-group Name: ")
id = cmd.security_group(sg_name)

#launch instance
instance_ID, availability_zone = cmd.launch_instances(id, keyname)

#Create EBS Volume
volume_ID = cmd.ebs_volume(availability_zone)

#Attach EBS to EC2
cmd.attach_ebs(instance_ID, volume_ID)
