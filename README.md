# Shopping Platform

store-hash: rmz2xgu42d

api doc:  https://developer.bigcommerce.com/docs/rest-management/customers-v2

postman：https://api.postman.com/collections/21830621-d9c5ebe2-8c6b-4de1-8e12-d92daffc7c6c?access_key=PMAT-01H1XV0PRJY3NPZNHMNCC4ZBPN

## 注册流程图

![bc注册](E:\Study\答辩\bc注册.png)

## 登录流程图

![bc登录](E:\Study\答辩\bc登录.png)

## 数据库设计ER图

![ER图](E:\Study\答辩\ER图.png)

## User Module

创建一个新用户需要以下参数（列表优化成对象）

```json
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
```

消费者表  customers

|     字段     | 数据类型 |              说明              |
| :----------: | :------: | :----------------------------: |
|      id      |   int    |           主键，自增           |
|  first_name  | varchar  |       用户首姓名，必填项       |
|  last_name   | varchar  |       用户次姓名，必填项       |
|    email     | varchar  |        邮箱，必填，唯一        |
|   company    | varchar  |          公司名，选填          |
|    phone     | varchar  |           电话，选填           |
| new_password | varchar  |              密码              |
|    bc_id     |   int    |       与bc店铺中的id对应       |
|  create_at   | datetime |    创建时间，创建时自动生成    |
|  update_at   | datetime | 更新时间，数据有更新时自动生成 |



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
|    customer_id    |   int    |            外键关联customers表的bc_id属性             |
|    address_id     |   int    |              与bc店铺中的address的id对应              |
|     create_at     | datetime |                  创建时间，自动生成                   |
|     update_at     | datetime |                  更新时间，自动生成                   |



## Product Module

商品分类表用于存储商品分类信息（商品需要有商品分类，才能在bc店铺显示）

创建一个商品分类至少需要以下数据

```
{
    "name": "test4",
    "parent_id": 0
}
```

|    字段    | 数据类型 |           说明           |
| :--------: | :------: | :----------------------: |
|     id     |   int    |        主键，自增        |
|    name    | varchar  |  分组名，唯一，不能为空  |
| parent_id  |   int    |     父分组名，默认0      |
| bc_cate_id |   int    | 与bc店铺中的分组的id对应 |
| create_at  | datetime |    创建时间，自动生成    |
| update_at  | datetime |    更新时间，自动生成    |



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

|    字段     | 数据类型 |                 说明                  |
| :---------: | :------: | :-----------------------------------: |
|     id      |   int    |              主键，自增               |
|    name     | varchar  |            商品名，必填项             |
|    type     | varchar  | 商品种类，digital或者physical，必填项 |
|   weight    | decimal  |            商品重量，必填             |
|    price    | decimal  |          商品价格，默认为35           |
|     sku     | varchar  |           商品的唯一性编号            |
| bc_prod_id  |   int    |         bc店铺中对应的商品id          |
| category_id |   int    |           商品种类id，外键            |
|  create_at  | datetime |          创建时间，自动生成           |
|  update_at  | datetime |          更新时间，自动生成           |



## Cart Module

每一个用户拥有一个购物车，需要一张购物车表，购物车与消费者是一对一关系，购物车表需要有一个customer_id与customer外键关联

购物车中需要存放加入购物车的商品信息，需要一张cartitem表，表中的一条记录存储一个购物车的一个商品，则需要一个cart_id外键关联购物车，还需要一个product_id外键关联商品表，还需要price字段存储商品的 价格信息，以及一个quantity字段存储加入购入车的每个条目的数量信息，

新增一条item的数据如下所示, 因为购物车id已经在路径中指定，所以只需要如下参数

```json
{
    "product_id": 147,
    "quantity": 7
}
```

表如下所示

|    字段    | 数据类型 |              说明               |
| :--------: | :------: | :-----------------------------: |
|     id     |   int    |           主键，自增            |
|  quantity  |   int    |          数量，默认为1          |
|   price    | decimal  |     价格，默认为0，两位小数     |
|  cart_id   |   int    |      与carts表的id外键关联      |
| product_id |   int    | 与products表的bc_pro_id外键关联 |
| create_at  | datetime |       创建时间，自动生成        |
| update_at  | datetime |       更新时间，自动创建        |

为用户新增购物车的操作只能操作一次，且购物车不能删除，只能删除购物车中的条目。更新购物车的操作没有单独定义api，而是在新增购物车条目时自动更新

新建一个购物车只需要将用户的id放在请求体中即可，购物车表如下所示

|      字段      | 数据类型 |            说明            |
| :------------: | :------: | :------------------------: |
|       id       |   int    |         主键，自增         |
|  customer_id   |   int    | 外键关联customers中的bc_id |
| total_quantity |   int    |    购物车中总的商品数量    |
|  total_price   | decimal  |      购物车中总的价格      |
|   create_at    | datetime |     创建时间，自动生成     |
|   update_at    | datetime |     更新时间，自动生成     |



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

orders表如下所示

|      字段      | 数据类型 |                             说明                             |
| :------------: | :------: | :----------------------------------------------------------: |
|       id       |   int    |                          主键，自增                          |
|  bc_order_id   |   int    |                  bc店铺的orderid，方便操作                   |
|     status     |  choice  |                        支付状态，0-14                        |
| total_quantity |   int    |                       订单中的总商品数                       |
|  total_price   | decimal  |                        订单中的总价格                        |
|  customer_id   |   int    |                 与customer中的bc_id外键关联                  |
|   address_id   |   int    | address为必须字段，账单地址，与address中的address_id外键关联 |
|   create_at    | datetime |                      创建时间，自动生成                      |
|   update_at    | datetime |                      更新时间，自动生成                      |

orderItem表是order得具体细节

需要有一个order_id与order外键关联

需要有一个product_id与product中得bc_prod_id外键关联

需要有一个quantity存储一条item的商品数量

需要有一个total_price存储一条item的总价

order_items表如下所示

|    字段     | 数据类型 |              说明              |
| :---------: | :------: | :----------------------------: |
|     id      |   int    |           主键，自增           |
|  quantity   |   int    |        条目中的商品数量        |
| total_price | decimal  |      一个条目中的商品总价      |
|  order_id   |   int    | 与order中的bc_order_id外键关联 |
| product_id  |   int    | 与product中的bc_pro_id外键关联 |
|  create_at  | datetime |       创建时间，自动生成       |
|  update_at  | datetime |       更新时间，自动生成       |

下单流程

实际情况中，从登录用户的购物车中下单，所以不考虑校验customer_id, product_id, 等情况

下单之后，订单无法改变，唯一能改变的只有订单的支付状态，所以更新订单的请求，只更改订单状态，除此之外只能删除订单

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

## 代码优化

### 缓存策略

为get请求设置缓存，可以减少响应时间

### 字典解构

```python
Products.objects.create(
                name=prod_data['name'],
                type=prod_data['type'],
                weight=prod_data['weight'],
                price=prod_data['price'],
                sku=prod_data['sku'],
                bc_pro_id=result.json()['data']['id'],
                category=category
            )
            
# 优化后
Products.objects.create(
    			# 字典解构
                **prod_data,
                bc_pro_id=result.json()['data']['id'],
                category=category
            )
```



### 优化循环

```python
# 更新本地数据库
            if 'first_name' in new_data:
                customer.first_name = new_data['first_name']
            if 'last_name' in new_data:
                customer.last_name = new_data['last_name']
            if 'phone' in new_data:
                customer.phone = new_data['phone']
            if 'company' in new_data:
                customer.company = new_data['company']
            if 'authentication' in new_data:
                customer.new_password = new_data.get('authentication', {}).get('new_password')
            
            
# 优化后
new_password = new_data.get('authentication', {}).get('new_password')
            if new_password is not None:
                customer.new_password = new_password
            new_data.pop('id', None)
            # 优化代码
            for key, value in new_data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
```



### 提取公共代码

例如新增customer

```python
new_customer = Customers.objects.create(
                first_name=customer_data['first_name'],
                last_name=customer_data['last_name'],
                email=customer_data['email'],
                phone=customer_data['phone'],
                company=customer_data['company'],
                new_password=customer_data.get('authentication', {}).get('new_password'),
                bc_id=response['data'][0]['id']
            )
            

# 提取代码
new_customer = create_customer_in_local_database(customer_data, response['data'][0].get('id'))

def create_customer_in_local_database(customer_data, bc_id):
    new_customer = Customers.objects.create(
        first_name=customer_data['first_name'],
        last_name=customer_data['last_name'],
        email=customer_data['email'],
        phone=customer_data['phone'],
        company=customer_data['company'],
        new_password=customer_data.get('authentication', {}).get('new_password'),
        bc_id=bc_id
    )
    return new_customer
```

