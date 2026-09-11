locals {
  k8s_dir = "${path.module}/../kubernetes"

  template_vars = {
    acr_login_server         = azurerm_container_registry.acr.login_server
    storage_connection_string = azurerm_storage_account.storage_account.primary_connection_string
  }
}

resource "local_file" "k8s_manifests" {
  for_each = fileset(local.k8s_dir, "*.tpl")

  filename = "${local.k8s_dir}/${trimsuffix(each.value, ".tpl")}"
  content  = templatefile("${local.k8s_dir}/${each.value}", local.template_vars)
}