locals {
  location         = "eu-central-1"
  environment      = "dev"
  project          = "ws2223"
  template_version = "0.0.1"
  team             = "andizzo"
  role             = "cloud02"
}

module "s3_bucket" {
  source = "./terraform-aws-modules/s3"
  providers = {
    aws = aws.ffm
  }

  environment      = local.environment
  role             = local.role
  template_version = local.template_version
  team             = local.team
}

module "sagemaker_notebook" {
  source = "./terraform-aws-modules/sagemaker_notebook"
  providers = {
    aws = aws.ffm
  }

  s3_bucket_name = module.s3_bucket.bucket_name
  file_name      = "picture.png"
  file_source    = "./picture.png"
  repository_url = "https://github.com/juic3pow3rs/terraform-aws-sagemaker-notebook.git"

  environment      = local.environment
  role             = local.role
  project          = local.project
  template_version = local.template_version
  team             = local.team
}