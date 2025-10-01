# DevOps Practice Paper

## Section A – MCQs

**Q1. (1 mark)**  
Which command is used to check the commit history in Git?  
- a) git status  
- b) git log  
- c) git history  
- d) git show  

**Answer:** b) git log  

**Q2. (1 mark)**  
Which AWS service is primarily used for object storage?  
- a) EC2  
- b) S3  
- c) EBS  
- d) IAM  

**Answer:** b) S3  

**Q3. (2 marks) (Choose 2)**  
Which are correct about Ansible?  
- a) Agentless tool  
- b) Uses YAML for playbooks  
- c) Requires Java to run  
- d) Only works on Windows  

**Answer:** a) Agentless tool, b) Uses YAML for playbooks  

**Q4. (1 mark)**  
Which command lists all Docker images available locally?  
- a) docker ps  
- b) docker images  
- c) docker run  
- d) docker list  

**Answer:** b) docker images  

**Q5. (2 marks) (Choose 2)**  
Which steps are required to push a custom Docker image to Docker Hub?  
- a) Tag the image with Docker Hub username  
- b) Run docker pull  
- c) Log in with docker login  
- d) Push using docker push  

**Answer:** a), c), d)  

**Q6. (1 mark)**  
Which command is used to remove all stopped containers at once?  
- a) docker rm -a  
- b) docker container prune  
- c) docker rmi  
- d) docker stop -all  

**Answer:** b) docker container prune  

**Q7. (2 marks) (Choose 2)**  
Which features make Terraform infrastructure as code?  
- a) Declarative configuration  
- b) Manual server setup  
- c) Resource provisioning through code  
- d) GUI-based infrastructure management  

**Answer:** a), c)  

**Q8. (1 mark)**  
In Jenkins, a Freestyle project allows you to:  
- a) Create Docker images  
- b) Build and test simple jobs with GUI-based configuration  
- c) Write Infrastructure as Code  
- d) Run Terraform commands automatically  

**Answer:** b) Build and test simple jobs with GUI-based configuration  

**Q9. (1 mark)**  
Which command is used to see the execution plan before applying Terraform changes?  
- a) terraform show  
- b) terraform init  
- c) terraform plan  
- d) terraform graph  

**Answer:** c) terraform plan  

**Q10. (2 marks) (Choose 2)**  
Which of the following plugins/tools can Jenkins integrate with?  
- a) GitHub  
- b) Terraform  
- c) Jenkins itself  
- d) Docker  

**Answer:** a), d)  

**Q11. (1 mark)**  
Which AWS service provides virtual servers in the cloud?  
- a) S3  
- b) EC2  
- c) IAM  
- d) CloudFormation  

**Answer:** b) EC2  

**Q12. (2 marks) (Choose 2)**  
Which are valid ways to secure AWS IAM accounts?  
- a) Multi-Factor Authentication (MFA)  
- b) Root account for daily use  
- c) Strong password policy  
- d) Sharing access keys with teammates  

**Answer:** a), c)  

**Q13. (1 mark)**  
Which command is used to run an Ansible playbook?  
- a) ansible-inventory  
- b) ansible-playbook  
- c) ansible-run  
- d) ansible-config  

**Answer:** b) ansible-playbook  

**Q14. (1 mark)**  
What is the main purpose of a CI/CD pipeline?  
- a) Monitoring system logs  
- b) Automating build, test, and deployment processes  
- c) Creating Docker containers  
- d) Managing infrastructure on AWS  

**Answer:** b) Automating build, test, and deployment processes  

**Q15. (1 mark)**  
If a container is stopped, which command can restart it?  
- a) docker kill  
- b) docker exec  
- c) docker start  
- d) docker build  

**Answer:** c) docker start  

**Q16. (2 marks) (Choose 2)**  
Which commands are used to undo changes in Git?  
- a) git revert  
- b) git push -f  
- c) git reset  
- d) git merge  

**Answer:** a), c)  

---

## Section B – Scenario-Based Questions (24 Marks)

**Q17. (6 marks)**  
Containerize an application using an httpd container. Create your own HTML files inside the container and serve them. After that, take a backup of the application by creating an image from the running container and upload this custom image to Docker Hub.  

![Deployment](images/docker.png)
![docker](Q1 DOCKER HISTORY.png)  

**Q18. (6 marks)**  
Create a new repository on GitHub where the default branch should be `main`. On your local machine, set up a repository with the same default branch (`main`), add multiple files, and push them to the GitHub repository. Ensure the branch alignment between local and remote is correct.  

![GitHub Repo](Q18%20GITHUB.png)  
![Local Repo](Q18%20LOCAL.png)  

**Q19. (6 marks)**  
Write Terraform configuration to create 2 EC2 instances in the North Virginia (us-east-1) region. Include all the parameters required to access the instances (AMI, instance type, key pair, security group, etc.). Use best practices such as variable files and separate resource definitions.  

![Terraform Main](Q19%20MAIN.TF.png)  
![Terraform Variables](Q19%20VARIABEL.TF.png)  
