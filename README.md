# Shopping Platform

store-hash: rmz2xgu42d

api doc:  https://developer.bigcommerce.com/docs/rest-management/customers-v2



## 总体概述

**用户表**用于保存用户信息



**地址表**用户存储地址信息

用户表与地址表之间用外键关联



**购物车表**用于存储购物车信息

购物车表与用户表和商品表用外键关联



**商品表**用于存储商品信息



**订单表**用于存储订单信息

**订单细节表**存储订单细节





# User Module

### 用户注册

创建一个新用户需要以下参数

```json

[
  {
    "email": "string@example2.com",
    "first_name": "string2",
    "last_name": "string2",
    "company": "string",
    "phone": "string",
    "notes": "string",
    "addresses": [
      {
        "address1": "Addr 1",
        "address2": "",
        "address_type": "residential",
        "city": "San Francisco",
        "company": "History",
        "country_code": "US",
        "first_name": "Ronald",
        "last_name": "Swimmer",
        "phone": "707070707",
        "postal_code": "33333",
        "state_or_province": "California"
      }
    ],
    "authentication": {
      "force_password_reset": true,
      "new_password": "string123"
    }
  }
]
```

最简请求体

```json
[
  {
    "email": "string@example2.com",
    "first_name": "string1",
    "last_name": "string1",
    "company": "string",
    "phone": "string",
    "authentication": {
      "new_password": "string123"
    }
  }
]
```



消费者表  customers

|     字段     | 数据类型 |        说明        |
| :----------: | :------: | :----------------: |
|      id      |   int    |     主键，自增     |
|  first_name  | varchar  | 用户首姓名，必填项 |
|  last_name   | varchar  | 用户次姓名，必填项 |
|    email     | varchar  |  邮箱，必填，唯一  |
|   company    | varchar  |    公司名，选填    |
|    phone     | varchar  |     电话，选填     |
| new_password | varchar  |        密码        |



用户地址表 address

|       字段        | 数据类型 |                         说明                          |
| :---------------: | :------: | :---------------------------------------------------: |
|        id         |   int    |                      主键，自增                       |
|     address1      | varchar  |                    地址栏1，必填项                    |
|     address2      | varchar  |                        地址栏2                        |
|   address_type    | varchar  | 地址类型（下拉框选择）（'residential', 'commercial'） |
|       city        | varchar  |                    城市名，必填项                     |
|      company      | varchar  |                        公司名                         |
|   country_code    | varchar  |            国家编号（下拉框选择），必填项             |
|    first_name     | varchar  |                  用户首姓名，必填项                   |
|     last_name     | varchar  |                  用户次姓名，必填项                   |
|       phone       | varchar  |                         电话                          |
|    postal_code    | varchar  |                   缴税编号，必填项                    |
| state_or_province | varchar  |            州或者省（下拉框选择），必填项             |
|    customer_id    |   int    |              外键关联customers表得id属性              |

