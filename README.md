# Shopping Platform

store-hash: rmz2xgu42d

api doc:  https://developer.bigcommerce.com/docs/rest-management/customers-v2

# User Module

### User Register

创建一个新用户需要以下参数

```json
{
    "_authentication": {
        "password": "hhhxxx123"
    },
    "company": "string",
    "email": "hhhxxx@test.com",
    "first_name": "hhhxxx",
    "last_name": "hhhxxx",
    "phone": "string",
    "store_credit": 0,
    "registration_ip_address": "string",
    "customer_group_id": 0,
    "notes": "string",
    "tax_exempt_category": "string"
}
```

