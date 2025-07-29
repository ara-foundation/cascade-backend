# Product Requirements Document (PRD)

## Оглавление
- [Product description](#Product description)
- [Architecture](#Architecture)
- [Tasks organisation]#Tasks organisation]

## Product description
Rest backend based on REST methods description

### REST methods description
json contains information about REST methods to use in code development
as key for each element is url for calling method
as value is important information for task realization
```json
[ 
  {"/": 
      { 
        "name": "general",
        "description": "for test service work", 
        "method": "GET",
        "Authentication": null,
        "params": null,
        "response_type": "json",
        "response": {"message": "CascadeFund API"}
        }
  },
  {"/user/access-token" : 
      { 
        "name": "token",
        "description": "for handle authorization", 
        "method": "POST",
        "Authentication": null,
        "params": {"code": "string"},
        "response_type": "json",
        "response": {
                      "id": "github_id",
                      "name": "user name",
                      "session": "hashed_access_token",
                      "avatar_url": "string"
                     }

      }
  },
  {"/user/info" : 
      { 
        "name": "user_info",
        "description": "Return user information for front", 
        "method": "GET",
        "Authentication": null,
        "params": {"hash": "string"},
        "response_type": "json",
        "response": {
                      "id": "github_id",
                      "name": "user name",
                      "session": "hashed_access_token",
                      "avatar_url": "string"
                     }
      }
  },
  {"/project/info/:slug" : 
      { 
        "name": "user_info",
        "description": "Return information about a project by it’s slug. Optionally it can skip some parts defined in the 'omit' query.",
        "method": "GET",
        "Authentication": null,
        "params": {"omit": "string that concatenate params  by ',' for example: param1,param2 "},
        "response_type": "json",
        "response": {
                      "meta": {
                        "title": "string",
                        "logo_url": "string",
                        "description": "string",
                        "rating": "number",
                        "is_lib": "boolean",
                        "purl": "string"
                      },
                      "maintainer": {
                        "withdraw_address": "string",
                        "cascade_withdraw_address": "string",
                        "name": "string",
                        "id": "string"
                      },
                      "source_code": {
                        "url": "string",
                        "added_date": "unix_timestamp",
                        "branch": "string possible values is  main or master"
                      },
                      "links": [ 
                        {
                          "label": "Telegram",
                          "url": "https://t.me/arasangha",
                          "icon": "fa-telegram"
                        }
                      ],
                      "sbom": [
                        {
                          "purl": "string",
                          "links": []
                        }
                      ],
                      "lib": {
                        "depends": "number, how many packages depends on this project"
                      },
                      "hyperpayment": {
                        "specification": "url",
                        "additional_contracts": [
                          {
                            "payment_gateway": {
                              "resource_type": "fixed|percent|dynamic",
                              "value": "float"
                            },
                            "blockchain_tx_fee": {
                              "resource_type": "fixed|percent|dynamic",
                              "value": "float"
                            }
                          }
                        ]
                      }
                    }
      }
  }
] 
```
 

## Architecture
Architecture description in json 
```json
{ 
  "programming_language": "python",
  "libraries": ["FastApi","pydentic"],
  "db": "mongoDb",
  "db_settings": ".env"
}
```

## Tasks organisation
path to main task file
docs/tasks/tasks.md

### Task flow
Tasks -> task analyze -> task solution 