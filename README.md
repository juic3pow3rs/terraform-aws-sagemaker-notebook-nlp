# terraform-aws-sagemaker-notebook

## Prerequisites
* aws account
* installed and configured awscli
* installed terraform

## Setup
1. Clone Repository with ```--recurse-submodules``` flag to pull sub-modules as well
2. Create S3-Bucket for your statefile
3. Update S3-Bucket Name in [state.tf](state.tf)
4. Update configuration in [main.tf](main.tf) to your needs
5. Run ```terraform init```, ```terrafrom plan``` & then ```terraform apply```
