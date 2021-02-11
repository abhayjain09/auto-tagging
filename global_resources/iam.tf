resource "aws_iam_role" "Auto-Tag-All-Resources" {
  name               = "Auto-Tag-All-Resources"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_iam_role_policy_attachment" "AdministratorAccess" {
  role =  aws_iam_role.Auto-Tag-All-Resources.id
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}


resource "aws_iam_role" "Lambda-invoke-role" {
  name               = "Lambda-invoke-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
lifecycle {
    create_before_destroy = true
  }

}

resource "aws_iam_role_policy_attachment" "AWSLambdaBasicExecutionRole" {
  role =  aws_iam_role.Lambda-invoke-role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "AWSLambdaRole" {
  role =  aws_iam_role.Lambda-invoke-role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
}

resource "aws_iam_role_policy_attachment" "AmazonEC2ReadOnlyAccess" {
  role =  aws_iam_role.Lambda-invoke-role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}



  

/*

resource "aws_iam_role_policy" "AdministratorAccess-policy" {
  name = "AdministratorAccess-policy"
  role = aws_iam_role.Auto-Tag-All-Resources.id
  policy =  <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }
    ]
}

EOF
}



resource "aws_iam_instance_profile" "EC2-instanceprofile" {
  name = "EC2ReadOnlyAccess-role"
  role = aws_iam_role.EC2ReadOnlyAccess-role.name
}
*/
