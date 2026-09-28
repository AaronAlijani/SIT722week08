terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstateaaron722"
    container_name       = "tfstate"
    key                  = "week08.tfstate"
  }
}