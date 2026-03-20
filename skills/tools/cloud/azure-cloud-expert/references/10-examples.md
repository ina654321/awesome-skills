# Examples

## 10.1 Resource Group Creation

```bash
# Create resource group
az group create --location eastus --name rg-webapp-prod

# Add tag to resource group
az group update --name rg-webapp-prod --set tags.Environment=Production tags.Team=Platform

# List resource groups
az group list --output table
```

## 10.2 VM Deployment

```bash
# Create VM with managed identity
az vm create \
  --resource-group rg-webapp-prod \
  --name vm-web-01 \
  --image UbuntuLTS \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --assign-identity

# Enable system managed identity on existing VM
az vm identity assign \
  --name vm-web-01 \
  --resource-group rg-webapp-prod
```

## 10.3 AKS Cluster Setup

```bash
# Create AKS cluster
az aks create \
  --resource-group rg-aks-prod \
  --name aks-prod-cluster \
  --node-count 3 \
  --enable-managed-identity \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --name aks-prod-cluster --resource-group rg-aks-prod

# Scale cluster
az aks scale --resource-group rg-aks-prod --name aks-prod-cluster --node-count 5
```

## 10.4 Azure SQL Deployment

```bash
# Create logical server
az sql server create \
  --name sql-webapp-prod \
  --resource-group rg-webapp-prod \
  --location eastus \
  --admin-user sqladmin \
  --admin-password <password>

# Create database
az sql db create \
  --resource-group rg-webapp-prod \
  --server sql-webapp-prod \
  --name webappdb \
  --service-objective S0

# Configure firewall rule
az sql server firewall-rule create \
  --resource-group rg-webapp-prod \
  --server sql-webapp-prod \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

## 10.5 ARM Template Deployment

```azuredeploy.json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "storageAccountName": {
      "type": "string"
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-04-01",
      "name": "[parameters('storageAccountName')]",
      "location": "[parameters('location')]",
      "kind": "StorageV2",
      "sku": {
        "name": "Standard_LRS"
      }
    }
  ]
}
```

```bash
# Deploy template
az deployment group create \
  --resource-group rg-webapp-prod \
  --template-file azuredeploy.json \
  --parameters storageAccountName=mywebappstorage
```

## 10.6 Azure Functions with Event Hub Trigger

```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.event_hub_message_trigger(
    arg_name="eventHubMessages",
    event_hub_name="my-event-hub",
    connection="EVENT_HUB_CONNECTION"
)
def main(eventHubMessages: func.EventHubEvent):
    for message in eventHubMessages:
        logging.info(f"Python Event Hub trigger processed: {message}")
```

## 10.7 Cosmos DB Setup

```bash
# Create Cosmos DB account
az cosmosdb create \
  --name my-cosmos-db \
  --resource-group rg-webapp-prod \
  --kind MongoDB \
  --server-version 4.2

# Create database
az cosmosdb mongodb database create \
  --account-name my-cosmos-db \
  --name webappdb \
  --resource-group rg-webapp-prod

# Create collection
az cosmosdb mongodb collection create \
  --account-name my-cosmos-db \
  --database-name webappdb \
  --name products \
  --resource-group rg-webapp-prod \
  --shard "productId"
```

## 10.8 Azure AD App Registration

```bash
# Create app registration
az ad app create \
  --display-name "Web App" \
  --identifier-uris "https://mywebapp.azurewebsites.net" \
  --web-redirect-uris "https://mywebapp.azurewebsites.net/.auth/login/aad/callback"

# Get app ID
appId=$(az ad app show --display-name "Web App" --query appId -o tsv)

# Create service principal
az ad sp create --id $appId

# Assign contributor role
az role assignment create \
  --assignee $appId \
  --role Contributor \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-webapp-prod
```

## 10.9 Azure Policy Assignment

```bash
# Create policy definition
az policy definition create \
  --name "require-tags" \
  --display-name "Require tags on resources" \
  --description "Enforces required tags on resources" \
  --rules '{"if":{"allOf":[{"field":"type","equals":"Microsoft.Resources/subscriptions/resourceGroups"},{"exists":false}]},"then":{"effect":"deny"}}' \
  --params '{"tagName":{"type":"String"}}'

# Assign policy
az policy assignment create \
  --name "require-tags-assignment" \
  --policy "require-tags" \
  --params '{"tagName":"Environment"}' \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-webapp-prod
```

## 10.10 Cost Alert Setup

```bash
# Create budget
az consumption budget create \
  --budget-name monthly-budget \
  --amount 1000 \
  --time-grain Monthly \
  --start-date 2024-01-01 \
  --resource-group rg-webapp-prod \
  --notifications '[{"enabled":true,"threshold":80,"operator":"GreaterThan","contactEmails":["team@example.com"]}]'
```