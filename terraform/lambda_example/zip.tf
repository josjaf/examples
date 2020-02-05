# Lambda without helpers example
data "archive_file" "moo" {
  type        = "zip"
  source_file = "${path.module}/index.py"
  output_path = "${path.module}/moo_organizations_lambda.zip"
}

### Lambda with Helpers example
data "template_file" "index" {
  template = file("${path.module}/index.py")
}

data "template_file" "helpers" {
  template = file("${path.module}/helpers.py")
}

data "archive_file" "foo" {
  type = "zip"

  # source_file = "${path.module}/index.py"
  output_path = "${path.module}/foo_organizations_lambda.zip"
  source {
    content  = data.template_file.helpers.rendered
    filename = "helpers.py"
  }

  source {
    content  = data.template_file.index.rendered
    filename = "index.py"
  }
}

