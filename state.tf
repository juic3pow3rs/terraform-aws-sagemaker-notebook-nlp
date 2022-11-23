terraform {
  backend "s3" {
    bucket   = "aiml-tf-state-bucket"
    key      = "sagemaker_notebook.tfstate"
    region   = "eu-central-1"
  }
}
