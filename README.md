# Create and Deploy a ML model using Google Cloud Run, Github Actions and Terraform


*In this post. I will explain how to expose an API from a trained model, use best CI/CD practices (Github Actions) and IaC (Terraform) to automate infrastructure creation.*


## Prerrequisites

- Docker Desktop 
- Git 
- Github Account
- Google Cloud Platform with owner permissions 


##  Google Cloud Run

[Cloud Run](https://cloud.google.com/run) is a serverless platform from [Google Cloud](https://cloud.google.com/) to deploy and run containers. Cloud Run can be used to serve Restful web APIs, WebSocket applications, or microservices connected by gRPC. 

In this project we will need:

 1. An IAM account with permissions to create a service account
 2. Cloud Storage Admin permissions
 3. Cloud Registry Admin permissions
 4. Google Cloud Run Admin permissions

### In case the API is not exposed for public access:

In the terraform/main.tf:

Remove the resource `"google_cloud_run_service_iam_member"  "run_all_users"`.  

<img width="675" alt="image" src="https://user-images.githubusercontent.com/39871126/195152688-dae361cd-a87f-4757-beb9-2899c3a32db9.png">


Ideally, you can set the iam accounts that can access this api using Google Cloud Run UI or using Terraform. This approach doesn't add any latency to the
customer because it uses built-in IAM roles and permissions from Google Cloud.


## Terraform 

[Terraform](https://www.terraform.io/) is a popular open-source tool for running infrastructure as code. It uses HCL which is a declarative language to declare infrastructure.
The basic flow is:

- **Terraform init**: Initializes the plugins, backend and many config files Terraform uses to keep tracking of the infrastructure.
- **Terraform plan**: Generates an execution plan for all the infrastructure which is in terraform/main.tf
- **Terraform apply**: Apply all the changes that were on the plan.

All steps are declared in the .github/workflows/workflow.yaml



## Run it locally

 1. Fork the [repo](https://github.com/AlvaroRaul7/fastapi-MlOps/)
 2. Clone it in your computer
 3. Run `docker build -t ml-api .` in the root of the project to build the image of the api.
 4. Run  ` docker run -d --name ml -p 80:8080 ml-api ` to create the container using ml-api image built.
 5. Open [localhost](http://localhost/docs) to test the project.
 6. On /predict/ post endpoint, you can use this body as an example:
 
   ```  
  {
"test_array": [
0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,0,0,1,1,1,0,1,0,1,0]

}
```
 7. You should expect a response 200 with a `"prediction": 0` which means the flight wasn't delayed.

## Deploy it

 1. Generate a Service Account key and upload it in Github Secrets as `GCLOUD_SERVICE_KEY`
 2. Push any change in the main branch
 3. That's it! :)

## Stress Testing

  1. On Mac `brew install wrk`
  2. Run `wrk -t12 -c200 -d45s -s request.lua https://mlops-api-backend-1-5gdi5qltoq-uc.a.run.app/predict/` to open 12 threads with 200 open http connections during 45 seconds.

### How can we improve the results

<img width="1054" alt="image" src="https://user-images.githubusercontent.com/39871126/195390648-94d3663d-7b7f-4abf-8e17-325e8ef9e0c3.png">



The best approach would be using horizontal scaling. in this case we can create a 2nd Google Cloud Run instance and use load balancing to distribute the traffic between both instances.

## SLO and SLIs

 1. Availability of 99.95% in the cloud run instance over a year which sets an error budget of 0.5% in case there is any problem in the gcp region.
 2. Latency under 200 ms given 50k requests over 45s 

 

 
