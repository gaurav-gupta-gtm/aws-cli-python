import subprocess
import json
import time

class awscmd:

    def key_pair(self,key_name):
        key_output=json.loads(subprocess.getoutput("aws ec2 create-key-pair --key-name {}".format(key_name)))
        key=key_output["KeyMaterial"]
        file1=open("key.pem","w")
        file1.writelines(key)
        file1.close()
        print("Key-pair created")
        print("----------------------------")

    def security_group(self,sg_name):
        sg_detail = json.loads(subprocess.getoutput("aws ec2 create-security-group --group-name {0}  --description \"Security group for SSH\" ".format(sg_name)))
        subprocess.getoutput("aws ec2 authorize-security-group-ingress --protocol tcp --port 22 --group-name {} --cidr 0.0.0.0/0".format(sg_name))
        print("Security Group created")
        print("----------------------------")
        return sg_detail["GroupId"]

    def launch_instances(self,sg_id, key_name):
        count = input("Enter the number of instance you want to launch: ")
        output = json.loads(subprocess.getoutput("aws ec2 run-instances --image-id ami-0e306788ff2473ccb --instance-type t2.micro --count {} --security-group-ids {} --key-name {}".format(count,sg_id,key_name)))
        print("Instance launched Successfully")
        print("----------------------------")
        return output["Instances"][0]["InstanceId"], output["Instances"][0]["Placement"]["AvailabilityZone"]

    def ebs_volume(self,zone):
        size=input("Enter size of Volume in GiB: ")
        volume_detail = json.loads(subprocess.getoutput("aws ec2 create-volume --availability-zone {} --size {}".format(zone, size)))
        time.sleep(10)
        print(volume_detail["VolumeId"])
        print("EBS Volume of " + size + "GiB created successfully")
        print("----------------------------")
        return volume_detail["VolumeId"]

    def attach_ebs(self,InstanceID, VolumeID):
        subprocess.getoutput("aws ec2 attach-volume --device /dev/sdf --instance-id {} --volume-id {} ".format(InstanceID, VolumeID))
        print("EBS Volume Attached")
        print("----------------------------")
        print("DONE")
