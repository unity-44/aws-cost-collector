#### Prerequesites

- AWS Account
-- AWS IAM User
-- AWS CLI


#### Script

- Check EC2 Instances
- Check RDS Instances
- Check Cost
- Send SNS (Mail)


#### Problems

- Schedule on Weekdays
    If the script is running on remote machine it could run with cronjobs. Alternatively if running on local machine it could utilize schedule or pycron but is then subsceptible for reboots etc.

- Multiple AWS Accounts
    I used the method to select the profile of the awscli. Other methods could make use of directly inputting the AWS Secret and Access Key on the start of the script.


#### Future Ideas

- Scrape EC2 and RDS Costs and automatically use them for calculation
- Inputs for Mail 