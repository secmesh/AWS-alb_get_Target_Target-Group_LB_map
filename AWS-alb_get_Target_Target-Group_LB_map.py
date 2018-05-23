import boto3
elbList = boto3.client('elbv2')
ec2 = boto3.resource('ec2')
import boto
import boto.utils
from boto.vpc import VPCConnection


client = boto3.client("ec2")
conn=boto.vpc.connect_to_region("us-west-2")

bals = elbList.describe_load_balancers()

x_file = open('/usr/local/bin/python_scripts/targets.txt', 'r')
t=list()
for i in x_file:
    i=i.split('\n',1)[0]
    t.append(i)
print t

q=list()
lb_arn_lst=list()
lb_name_lst=list()
lb_target_group_arn_lst=list()
lb_target_group_name_lst=list()
dict_lb_arn={}
lst_for_final_alb=list()

##Below Lines will take the Name of the instances you've entered in the "targets.txt" file and print out their relevant Names(Tag Names)##

reservations = conn.get_all_reservations()
for s in reservations:
    for m in t:
            if 'Name' not in s.instances[0].tags:continue
            else:
                 if m in s.instances[0].tags['Name']: q.append(s.instances[0].id)
                 else: continue

##Below For Loop will get the Load balancer ARNs and Names and store them in two different Lists##


for i in bals['LoadBalancers']:
    lb_arn_lst.append(i['LoadBalancerArn'])
    lb_name_lst.append(i['LoadBalancerName'])



##Below For Loop will take the Load Balancer ARN from the List and extract the Target Group ARN associated with the ALB and store the Target Group ARN in a List##

for i in lb_arn_lst:
    response = elbList.describe_target_groups(
           LoadBalancerArn=i
    )
    for i in response['TargetGroups']:
#        print i['TargetGroupArn']
        lb_target_group_name_lst.append(i['TargetGroupName'])
        lb_target_group_arn_lst.append(i['TargetGroupArn'])

##Below For Loop will Take the Target GRoup ARN and extract the Instance ID assocaited with the Target Group(Target)##

for i in lb_target_group_arn_lst:
        response = elbList.describe_target_health(
        TargetGroupArn=i
        )
        for a in response['TargetHealthDescriptions']:
            for j in q:
                if j in a['Target']['Id']:
                     dict_lb_arn[i]=a['Target']['Id']
                     print "Instance ID is: ",j
                else: continue

##Below For Loop will Take Target information, find the Target Group Name, store it in a List and will Print the name of the Target Group ARN##

for k,v in dict_lb_arn.items():
    for i in lb_arn_lst:
        response = elbList.describe_target_groups(
               LoadBalancerArn=i
        )
        for j in response['TargetGroups']:
            if k in j['TargetGroupArn']:
                 lst_for_final_alb.append(i)
                 print "Target Group Name is: ",j['TargetGroupName']
            else: continue

##Below For Loop will Take the Target Group ARN, extract the Load Balancer Name and Print it Out##

for i in bals['LoadBalancers']:
    for j in lst_for_final_alb:
        if i['LoadBalancerArn'] in j: print "Load Balancer Name is: ",i['LoadBalancerName']
        else: continue
