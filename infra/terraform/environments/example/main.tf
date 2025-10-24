terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.118"
    }
  }
}

provider "azurerm" {
  features {}
}

# Placeholder resource to demonstrate directory structure.
resource "azurerm_resource_group" "example" {
  name     = "luxor9-example-rg"
  location = "eastus"
  tags = {
    project = "luxor9"
    env     = "example"
  }
}
