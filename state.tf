terraform {
  backend "s3" {
    bucket = "nlp-tf-state-bucket"
    key    = "sagemaker_notebook_nlp.tfstate"
    region = "eu-central-1"
    profile = "NLP"
  }
}
