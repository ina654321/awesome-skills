# Examples

## 10.1 阿里云域名注册与解析

```python
# 购买域名后设置DNS解析
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest

client = CommonACNClient('cn-hangzhou')

# 添加A记录
add_req = AddDomainRecordRequest.AddDomainRecordRequest()
add_req.set_DomainName('yourdomain.com')
add_req.set_RR('www')
add_req.set_Type('A')
add_req.set_Value('1.2.3.4')
add_req.set_TTL('600')  # TTL 10分钟

response = client.do_action_with_exception(add_req)
record_id = response['RecordId']
print(f"解析记录ID: {record_id}")
```

## 10.2 DNS解析配置

```bash
# 使用阿里云CLI配置DNS
aliyun alidns AddDomainRecord \
  --DomainName yourdomain.com \
  --RR www \
  --Type A \
  --Value 1.2.3.4 \
  --TTL 600

# 添加多条记录
aliyun alidns AddDomainRecord --DomainName yourdomain.com --RR @ --Type A --Value 1.2.3.4
aliyun alidns AddDomainRecord --DomainName yourdomain.com --RR mail --Type MX --Value "10 mail.yourdomain.com"
aliyun alidns AddDomainRecord --DomainName yourdomain.com --RR @ --Type TXT --Value "v=spf1 include:_spf.yourdomain.com ~all"
```

## 10.3 备案信息查询

```python
# 查询备案状态
from aliyunsdkbeian.request.v20170306 import Query备案信息Request

req = Query备案信息Request.Query备案信息Request()
req.set_备案类型('ICP')
response = client.do_action_with_exception(req)
print(f"备案状态: {response['备案状态']}")
print(f"审核信息: {response['审核信息']}")
```

## 10.4 域名转出流程

```
1. 在阿里云域名控制台解锁域名
2. 获取转移密码(授权码)
3. 到新注册商提交转入申请
4. 原注册商确认转出(5天内)
5. 新注册商完成转入

注意:
- 域名注册满60天后才能转出
- 距到期日大于15天才能转出
- 转出免费，但新注册商可能收取转入费
```

## 10.5 SSL证书自动部署到OSS

```python
# 通过阿里云CLI部署证书
aliyun oss cp cert.pem oss://my-bucket/cert/ --force
aliyun oss cp key.pem oss://my-bucket/cert/ --force

# 使用CDN时配置证书
from aliyunsdkcdn.request.v20180510 import SetCdnDomainSSLCertificateRequest

req = SetCdnDomainSSLCertificateRequest.SetCdnDomainSSLCertificateRequest()
req.set_DomainName('assets.yourdomain.com')
req.set_CertType('upload')
req.set_SSLProtocol('on')
req.set_ServerCertificate('-----BEGIN CERTIFICATE-----...')
req.set_ServerCertificateKey('-----BEGIN RSA PRIVATE KEY-----...')

client.do_action_with_exception(req)
```
