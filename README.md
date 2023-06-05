# Shopping Platform

store-hash: rmz2xgu42d

api doc:  https://developer.bigcommerce.com/docs/rest-management/customers-v2



# User Module

创建一个新用户需要以下参数（列表优化成对象）

```json
[
  {
    "email": "string@test88.com",
    "first_name": "hahaha",
    "last_name": "xxx",
    "company": "string",
    "phone": "string",
    "authentication": {
      "new_password": "string666"
    }
  }
]
```

消费者表  customers

|     字段     | 数据类型  |              说明              |
| :----------: | :-------: | :----------------------------: |
|      id      |    int    |           主键，自增           |
|  first_name  |  varchar  |       用户首姓名，必填项       |
|  last_name   |  varchar  |       用户次姓名，必填项       |
|    email     |  varchar  |        邮箱，必填，唯一        |
|   company    |  varchar  |          公司名，选填          |
|    phone     |  varchar  |           电话，选填           |
| new_password |  varchar  |              密码              |
|    bc_id     |    int    |       与bc店铺中的id对应       |
|  create_at   | timestamp |    创建时间，创建时自动生成    |
|  update_at   | timestap  | 更新时间，数据有更新时自动生成 |



消费者表与地址表为一对多关系，一个消费者可以有多条地址记录，一条地址记录只能被一个消费者拥有，

为消费者添加一个地址需要用到以下字段

```json
{
    "address1": "四川省绵阳市",
    "address2": "哈哈哈",
    "address_type": "residential",
    "city": "四川",
    "company": "四川省绵阳市/Delbert",
    "country": "China",
    "country_code": "CN",
    "customer_id": 74,
    "first_name": "Delbert",
    "last_name": "Liu",
    "phone": "123434",
    "postal_code": "4675345",
    "state_or_province": "四川"
}
```

用户地址表 address

|       字段        | 数据类型  |                         说明                          |
| :---------------: | :-------: | :---------------------------------------------------: |
|        id         |    int    |                      主键，自增                       |
|     address1      |  varchar  |                    地址栏1，必填项                    |
|     address2      |  varchar  |                        地址栏2                        |
|   address_type    |  varchar  | 地址类型（下拉框选择）（'residential', 'commercial'） |
|       city        |  varchar  |                    城市名，必填项                     |
|      company      |  varchar  |                        公司名                         |
|   country_code    |  varchar  |            国家编号（下拉框选择），必填项             |
|    first_name     |  varchar  |                  用户首姓名，必填项                   |
|     last_name     |  varchar  |                  用户次姓名，必填项                   |
|       phone       |  varchar  |                         电话                          |
|    postal_code    |  varchar  |                   缴税编号，必填项                    |
| state_or_province |  varchar  |            州或者省（下拉框选择），必填项             |
|    customer_id    |    int    |            外键关联customers表的bc_id属性             |
|    address_id     |    int    |              与bc店铺中的address的id对应              |
|     create_at     | timestamp |                  创建时间，自动生成                   |
|     update_at     | timestamp |                  更新时间，自动生成                   |



## Customer api 接口及数据

### 用户登录下发token

```
POST: http://127.0.0.1:8000/shop/api/v1/login/
数据：
{
    "email": "albertliu@163.com",
    "password": "albertliu123"
}
```



### 新增用户

```
POST: http://127.0.0.1:8000/shop/api/v1/customers
数据:
[
  {
    "email": "string@test88.com",
    "first_name": "hahaha",
    "last_name": "xxx",
    "company": "string",
    "phone": "string",
    "authentication": {
      "new_password": "string666"
    }
  }
]
```



### 查询所有用户

```
GET: http://127.0.0.1:8000/shop/api/v1/customers
```



### 更新用户信息

```
PUT: http://127.0.0.1:8000/shop/api/v1/customers/
查询参数: id: 1
数据：
[
  {
    "id": 62,
    "first_name": "string212",
    "last_name": "string212",
    "authentication": {
        "new_password": "string12122"
    }
  }
]
```



### 删除用户信息

```
DELETE: http://127.0.0.1:8000/shop/api/v1/customers/
查询参数： ids: 4,5,6
```



## Address api接口及数据

### 查询所有地址信息

```
GET: http://127.0.0.1:8000/shop/api/v1/customers/addresses
```



### 新增用户地址信息

```
POST: http://127.0.0.1:8000/shop/api/v1/customers/addresses/
数据：
{
    "address1": "四川省绵阳市",
    "address2": "哈哈哈",
    "address_type": "residential",
    "city": "四川",
    "company": "四川省绵阳市/Delbert",
    "country": "China",
    "country_code": "CN",
    "customer_id": 74,
    "first_name": "Delbert",
    "last_name": "Liu",
    "phone": "123434",
    "postal_code": "4675345",
    "state_or_province": "四川"
}
```



### 更新地址信息

```
PUT: http://127.0.0.1:8000/shop/api/v1/customers/addresses/
数据：
{
    "id": 24,
    "postal_code": "66667777"
}
```



### 删除用户地址信息

```
DELETE: http://127.0.0.1:8000/shop/api/v1/customers/addresses/
查询参数： ids: 4,5,6
```



# Product Module

商品分类表用于存储商品分类信息（商品需要有商品分类，才能在bc店铺显示）

创建一个商品分类至少需要以下数据

```
{
    "name": "test4",
    "parent_id": 0
}
```

|    字段    | 数据类型  |           说明           |
| :--------: | :-------: | :----------------------: |
|     id     |    int    |        主键，自增        |
|    name    |  varchar  |  分组名，唯一，不能为空  |
| parent_id  |    int    |     父分组名，默认0      |
| bc_cate_id |    int    | 与bc店铺中的分组的id对应 |
| create_at  | timestamp |    创建时间，自动生成    |
| update_at  | timestamp |    更新时间，自动生成    |



商品表用于存储商品的信息

创建一个商品表至少需要以下信息：（bc店铺接口中的数据, 商品分类应该是一个数组，要修改）

```
{
    "name": "HHH333",
    "type": "digital",
    "weight": 0,
    "price": 12.99,
    "sku": "HHH-333",
    "category": "test1"
}
```

|    字段     | 数据类型  |                 说明                  |
| :---------: | :-------: | :-----------------------------------: |
|     id      |    int    |              主键，自增               |
|    name     |  varchar  |            商品名，必填项             |
|    type     |  varchar  | 商品种类，digital或者physical，必填项 |
|   weight    |  decimal  |            商品重量，必填             |
|    price    |  decimal  |          商品价格，默认为35           |
|     sku     |  varchar  |           商品的唯一性编号            |
| bc_prod_id  |    int    |         bc店铺中对应的商品id          |
| category_id |    int    |           商品种类id，外键            |
|  create_at  | timestamp |          创建时间，自动生成           |
|  update_at  | timestamp |          更新时间，自动生成           |



## Product api接口及数据

### 获取所有商品分类

```
GET: http://127.0.0.1:8000/shop/api/v1/categories/
```



### 新增商品分类

```
POST: http://127.0.0.1:8000/shop/api/v1/categories/
数据：
{
    "name": "test4",
    "parent_id": 0
}
```



### 更新商品种类

```
PUT: http://127.0.0.1:8000/shop/api/v1/categories/
查询参数： id: 2
数据：
{
    "name": "test444",
    "parent_id": 0
}
```



### 删除商品种类

```
DELETE: http://127.0.0.1:8000/shop/api/v1/categories/
查询参数： id: 2
```



## Cart Module

每一个用户拥有一个购物车，需要一张购物车表，购物车与消费者是一对一关系，购物车表需要有一个customer_id与customer外键关联

购物车中需要存放加入购物车的商品信息，需要一张cartitem表，表中的一条记录存储一个购物车的一个商品，则需要一个cart_id外键关联购物车，还需要一个product_id外键关联商品表







## Order Module

创建一个订单需要如下内容

```
{
  "status_id": 10,
  "customer_id": 75,
  "billing_address": {
    "first_name": "Jane",
    "last_name": "Doe",
    "street_1": "123 Main Street",
    "city": "Austin",
    "state": "Texas",
    "zip": 78751,
    "country": "United States",
    "country_iso2": "US",
    "email": "janedoe@example.com"
  },
  "products": [
    {
      "product_id": "129",
      "quantity": "3"
    },
    {
      "product_id": "131",
      "quantity": "5"
    }
  ]
}
```

order表需要有一个customer_id外键关联customer中得bc_id

需要有一个status_id是一个choice，用于展示订单状态

需要address_id与address中得与bc店铺中address得id对应得address_id

需要一个total_quantity 存储订单中商品总数量

需要一个total_price 存储订单中商品总价



orderItem表是order得具体细节

需要有一个order_id与order外键关联

需要有一个product_id与product中得bc_prod_id外键关联

需要有一个quantity存储一条item的商品数量

需要有一个total_price存储一条item的总价

### order status

| Status ID | Name                         | Description                                                  |
| --------- | ---------------------------- | ------------------------------------------------------------ |
| 0         | Incomplete                   | An incomplete order happens when a shopper reached the payment page, but did not complete the transaction. |
| 1         | Pending                      | Customer started the checkout process, but did not complete it. |
| 2         | Shipped                      | Order has been shipped, but receipt has not been confirmed; seller has used the Ship Items action. |
| 3         | Partially Shipped            | Only some items in the order have been shipped, due to some products being pre-order only or other reasons. |
| 4         | Refunded                     | Seller has used the Refund action.                           |
| 5         | Cancelled                    | Seller has cancelled an order, due to a stock inconsistency or other reasons. |
| 6         | Declined                     | Seller has marked the order as declined for lack of manual payment, or other reasons. |
| 7         | Awaiting Payment             | Customer has completed checkout process, but payment has yet to be confirmed. |
| 8         | Awaiting Pickup              | Order has been pulled, and is awaiting customer pickup from a seller-specified location. |
| 9         | Awaiting Shipment            | Order has been pulled and packaged, and is awaiting collection from a shipping provider. |
| 10        | Completed                    | Client has paid for their digital product and their file(s) are available for download. |
| 11        | Awaiting Fulfillment         | Customer has completed the checkout process and payment has been confirmed. |
| 12        | Manual Verification Required | Order is on hold while some aspect needs to be manually confirmed. |
| 13        | Disputed                     | Customer has initiated a dispute resolution process for the PayPal transaction that paid for the order. |
| 14        | Partially Refunded           | Seller has partially refunded the order.                     |
