## Requirements

The following requirements are needed by this module:

- terraform (~> 0.13.0)

- archive (~> 1.0)

- aws (~> 3.0)

- random (~> 2.0)

## Providers

The following providers are used by this module:

- archive (~> 1.0)

- aws (~> 3.0)

- random (~> 2.0)

## Required Inputs

The following input variables are required:

### bucket

Description: The S3 bucket location for the function's deployment package.

Type: `string`

### handler

Description: The function entrypoint in your code.

Type: `string`

### name

Description: The name of the Lambda function.

Type: `string`

### runtime

Description: The runtime for lambda ie python3.8, nodejs12.x, go1.x, dotnetcore3.1, java11.

Type: `string`

### source\_dir

Description: Package entire contents of this directory into the Lambda archive.

Type: `string`

## Optional Inputs

The following input variables are optional (have default values):

### enable\_active\_tracing

Description: If true, enables active tracing. The default false sets it to pass through mode.

Type: `bool`

Default: `false`

### egress\_security\_groups

Description: A list of egress security group IDs to associate with.

Type: `list(string)`

Default: `[]`

### layers

Description: List of Lambda Layer Version ARNs (maximum of 5) to attach to your Lambda function.

Type: `list(string)`

Default: `[]`

### policy\_arns

Description: List of IAM Policy ARNs for Lambda role.  \*\*\* Use only pre-existing policies \*\*\*

Type: `list(string)`

Default:

```json
[
  "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
  "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess",
  "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
]
```

### policy\_documents

Description: List of IAM Policy Documents for Lambda role.

Type: `list(string)`

Default: `[]`

### env

Description: A map that defines environment variables for the Lambda function.

Type: `map(string)`

Default: `null`

### tags

Description: Additional tags associated with Lambda.

Type: `map(string)`

Default: `{}`

### maximum\_event\_age\_in\_seconds

Description: Maximum age of a request that Lambda sends to a function for processing in seconds.

Type: `number`

Default: `null`

### maximum\_retry\_attempts

Description: Maximum number of times to retry when the function returns an error.

Type: `number`

Default: `null`

### memory\_size

Description: Amount of memory in MB your Lambda Function can use at runtime. Defaults to 128.

Type: `number`

Default: `null`

### reserved\_concurrent\_executions

Description: The amount of reserved concurrent executions. 0 disables lambda and -1 removes any limit.

Type: `number`

Default: `null`

### timeout

Description: The amount of time your Lambda Function has to run in seconds. Defaults to 60.

Type: `number`

Default: `60`

### on\_success\_destination

Description: ARN of destination resource - SNS, Lambda or SQS.

Type: `string`

Default: `null`

### vpc\_name

Description: The name of the VPC in which the instance should be deployed.

Type: `string`

Default: `null`

## Outputs

The following outputs are exported:

### arn

Description: n/a

### dead\_letter\_queue\_arn

Description: n/a

### invoke\_policy

Description: n/a

### name

Description: n/a

### role

Description: The details for the Lambda role.

