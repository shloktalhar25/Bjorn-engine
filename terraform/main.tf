# here we would write the actual code for creating the s3 bucket


resource "aws_s3_bucket" "data_lake" {
  bucket = var.bucket_name

  tags = {
    Name        = "Data Lake"
    Environment = "Development"
  }
}

