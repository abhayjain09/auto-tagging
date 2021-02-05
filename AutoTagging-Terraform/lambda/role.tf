module "role" {
  source           = "../role"
  name             = "${var.name}-lambda"
  description      = "${var.name} Lambda Role"
  tags             = local.tags
  service          = "lambda"
  policy_arns      = var.policy_arns
  policy_documents = concat(var.policy_documents, [module.dead-letter-queue.write_policy.document])
}
