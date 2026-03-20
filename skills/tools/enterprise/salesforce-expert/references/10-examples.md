# Examples

## 10.1 Basic SOQL

```sql
-- Query accounts
SELECT Id, Name, Industry, AnnualRevenue 
FROM Account 
WHERE Industry = 'Technology'
ORDER BY AnnualRevenue DESC
LIMIT 10

-- Query with related records
SELECT Name, (SELECT Name FROM Contacts) 
FROM Account
```

## 10.2 Apex Trigger

```apex
trigger AccountTrigger on Account (before insert, before update) {
    if (Trigger.isBefore) {
        for (Account acc : Trigger.new) {
            if (acc.Industry == 'Technology' && acc.AnnualRevenue == null) {
                acc.AnnualRevenue = 0;
            }
        }
    }
}
```

## 10.3 Batch Apex

```apex
global class ProcessAccounts implements Database.Batchable<sObject> {
    global Database.QueryLocator start(Database.BatchableContext bc) {
        return Database.getQueryLocator('SELECT Id, Name FROM Account WHERE Industry = \'Tech\'');
    }
    
    global void execute(Database.BatchableContext bc, List<Account> scope) {
        for (Account a : scope) {
            a.Industry = 'Technology';
        }
        update scope;
    }
    
    global void finish(Database.BatchableContext bc) {
        System.debug('Batch complete');
    }
}

// Execute
Database.executeBatch(new ProcessAccounts(), 200);
```

## 10.4 LWC Component

```javascript
// myComponent.js
import { LightningElement, api } from 'lwc';

export default class MyComponent extends LightningElement {
    @api recordId;
    
    handleClick() {
        console.log('Clicked: ' + this.recordId);
    }
}
```

```html
<!-- myComponent.html -->
<template>
    <lightning-card title="My Card">
        <lightning-button label="Click" onclick={handleClick}></lightning-button>
    </lightning-card>
</template>
```

## 10.5 REST API Callout

```apex
public class ExternalService {
    public static void callEndpoint() {
        Http http = new Http();
        HttpRequest request = new HttpRequest();
        request.setEndpoint('https://api.example.com/data');
        request.setMethod('GET');
        request.setHeader('Authorization', 'Bearer ' + UserInfo.getSessionId());
        
        HttpResponse response = http.send(request);
        System.debug(response.getBody());
    }
}
```

## 10.6 Flow Builder - Record Triggered

```xml
<!-- Flow XML -->
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>Flow to update account</description>
    <label>Update Account</label>
    <status>Active</status>
    <triggerType>RecordBeforeSave</triggerType>
    <object>Account</object>
</Flow>
```

## 10.7 Test Class

```apex
@isTest
private class AccountTriggerTest {
    @TestSetup
    static void setup() {
        Account acc = new Account(Name = 'Test Account');
        insert acc;
    }
    
    @isTest
    static void testTrigger() {
        Account acc = [SELECT Name FROM Account WHERE Name = 'Test Account'];
        acc.Industry = 'Technology';
        update acc;
        
        Account updated = [SELECT Industry FROM Account WHERE Id = :acc.Id];
        System.assertEquals('Technology', updated.Industry);
    }
}
```