module "dead-letter-queue" {
  source = "../sqs-queue"
  name   = "${var.name}-dead-letter-queue"
  tags   = var.tags
}
