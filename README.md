## Usage

How to use aws-cost-collector:

- Clone or download git repo
- Make sure you have aws-cli installed and configured
- Set ARN for SNS (to be configured in AWS)
- Run script.py

#### Prerequesites

- AWS Account
- AWS IAM User (Key)
- AWS CLI

#### Script

- Check EC2 Instances
- Check RDS Instances
- Check Cost
- Send SNS (Mail)
- Create History


#### Problems

  

- Schedule on Weekdays

If the script is running on remote machine it could run with cronjobs. Alternatively if running on local machine it could utilize schedule or pycron but is then subsceptible for reboots etc.

Another Solution might be to run everything as AWS Lambda function and schedule with CloudWatch

  

- Multiple AWS Accounts

I used the method to select the profile of the awscli. Other methods could make use of directly inputting the AWS Secret and Access Key on the start of the script.

- Cloudformation

I think my current setup would work better in AWS Lambda then in Cloudformation. Also collecting costs is easier with AWS CostExplorer


#### Future Ideas

  
- Scrape EC2 and RDS Costs and automatically use them for calculation
- Inputs for Mail
- Do not use cost calculation with EC2 and RDS but use AWS CostExplorer to get metrics and costs
