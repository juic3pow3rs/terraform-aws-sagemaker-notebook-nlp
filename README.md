# terraform-aws-sagemaker-notebook

## Prerequisites
* aws account
* installed and configured awscli
* installed terraform

## Configure AWS CLI
1. Login to AWS and click "Command line or programmatic access"
2. Run ```aws configure sso --profile NLP```
3. IMPORTANT: When promted for "sso session name" leave it empty!
4. Other than that enter the details asked
5. At some point a browser tab will open with a code which you need to confirme
6. Edit your ```.aws/config``` and add ```sso_start_url```, ```sso_region``` as well as ```region```
7. Login via ```aws sso login --profile NLP```
8. Set your AWS profile as environment variable via ```export AWS_PROFILE=NLP```


## Setup
1. Clone Repository with ```--recurse-submodules``` flag to pull sub-modules as well
5. Run ```terraform init```, ```terrafrom plan``` & then ```terraform apply```

## Note multiple deployments are not possible unless some modifications in the naming and the state.