# Examples

## 10.1 ECS + RDS + OSS架构

```
用户 → CDN → OSS(静态资源)
           ↓
        ECS(Web服务)
           ↓
        RDS(数据库) + Redis(缓存)
```

## 10.2 Python SDK创建ECS

```python
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest

client = CommonACNClient('cn-hangzhou')

# 创建实例
create_req = CreateInstanceRequest.CreateInstanceRequest()
create_req.set_ImageId('aliyun_2_1903_x64_20G_alibase_20231220.vc')
create_req.set_InstanceType('ecs.s6-c1m2.small')
create_req.set_SecurityGroupId('sg-xxxxx')
create_req.set_VSwitchId('vsw-xxxxx')
create_req.set_InstanceChargeType('PostPaid')
create_req.set_SystemDiskCategory('cloud_ssd')

instance_id = client.do_action_with_exception(create_req)
print(f"实例ID: {instance_id}")

# 启动实例
start_req = StartInstanceRequest.StartInstanceRequest()
start_req.set_InstanceId(instance_id)
client.do_action_with_exception(start_req)
```

## 10.3 Terraform部署ECS

```hcl
provider "alicloud" {
  region = "cn-hangzhou"
}

resource "alicloud_instance" "web" {
  image_id        = "aliyun_2_1903_x64_20G_alibase_20231220.vc"
  instance_type   = "ecs.s6-c1m2.small"
  security_groups = [alicloud_security_group.default.id]
  vswitch_id      = alicloud_vswitch.default.id
  
  system_disk_category = "cloud_ssd"
  system_disk_size    = 40
  
  internet_charge_type = "PayByBandwidth"
  internet_max_bandwidth_out = 5
  
  instance_name = "web-server"
}

resource "alicloud_security_group" "default" {
  name = "web-sg"
  
  ingress {
    protocol = "tcp"
    port     = "80"
    cidr_ip  = "0.0.0.0/0"
  }
  
  egress {
    protocol = "all"
    cidr_ip  = "0.0.0.0/0"
  }
}
```

## 10.4 成本优化实践

```python
# 查询预留实例券
from aliyunsdkecs.request.v20140526 import DescribeReservedInstancesRequest

req = DescribeReservedInstancesRequest.DescribeReservedInstancesRequest()
req.set_ZoneId('cn-hangzhou-h')
req.set_OfferingType('No Upfront')

response = client.do_action_with_exception(req)
for instance in response['ReservedInstances']:
    print(f"券ID: {instance['ReservedInstanceId']}, 规格: {instance['InstanceType']}")
```

## 10.5 资源标签管理

```python
# 为ECS添加标签
from aliyunsdkecs.request.v20140526 import AddTagsRequest

req = AddTagsRequest.AddTagsRequest()
req.set_ResourceType('instance')
req.set_ResourceId('i-xxxxx')
req.set_Tags([{'TagKey': 'Environment', 'TagValue': 'Production'}])
```
