# Examples

## 10.1 添加CDN加速域名 (Python SDK)

```python
from aliyunsdkcdn.request.v20180510 import AddCdnDomainRequest

client = CommonACNClient('cn-shanghai')
request = AddCdnDomainRequest.AddCdnDomainRequest()
request.set_DomainName('assets.yourdomain.com')
request.set_CdnType('web')
request.set_SourceType('oss')
request.set_SourcePort(80)
request.set_Sources('yourbucket.oss-cn-shanghai.aliyuncs.com')

response = client.do_action_with_exception(request)
print(response.decode('utf-8'))
```

## 10.2 配置缓存过期规则

```python
from aliyunsdkcdn.request.v20180510 import SetCacheConfigRequest

# 设置静态资源缓存30天
request = SetCacheConfigRequest.SetCacheConfigRequest()
request.set_DomainName('assets.yourdomain.com')
request.set_ConfigType('cache expired')
request.set_Key('jpg;jpeg;png;gif;css;js')
request.set_TTL('31536000')
request.set_Weight('1')

client.do_action_with_exception(request)
```

## 10.3 刷新CDN缓存

```python
from aliyunsdkcdn.request.v20180510 import PushObjectCacheRequest, RefreshObjectCachesRequest

client = CommonACNClient('cn-shanghai')

# 刷新单个文件
refresh_request = RefreshObjectCachesRequest.RefreshObjectCachesRequest()
refresh_request.set_ObjectPath('https://assets.yourdomain.com/image.jpg')
refresh_request.set_ObjectType('File')
response = client.do_action_with_exception(refresh_request)
print(response)

# 预热(提前缓存热门资源)
push_request = PushObjectCacheRequest.PushObjectCacheRequest()
push_request.set_ObjectPath('https://assets.yourdomain.com/promo/video.mp4')
response = client.do_action_with_exception(push_request)
```

## 10.4 配置HTTPS证书

```python
from aliyunsdkcdn.request.v20180510 import SetCdnDomainSSLCertificateRequest

request = SetCdnDomainSSLCertificateRequest.SetCdnDomainSSLCertificateRequest()
request.set_DomainName('assets.yourdomain.com')
request.set_CertType('upload')
request.set_SSLProtocol('on')
request.set_CertName('my-cert')
request.set_ServerCertificate('-----BEGIN CERTIFICATE-----...')
request.set_ServerCertificateProtocol('HTTPS')

client.do_action_with_exception(request)
```

## 10.5 查询CDN实时访问日志

```python
from aliyunsdkcdn.request.v20180510 import DescribeCdnLogRequest

request = DescribeCdnLogRequest.DescribeCdnLogRequest()
request.set_DomainName('assets.yourdomain.com')
request.set_LogType('cdn')
request.set_PageSize(100)
request.set_PageNumber(1)

response = client.do_action_with_exception(request)
# 返回日志文件列表和下载地址
```

## 10.6 配置Referer防盗链

```python
from aliyunsdkcdn.request.v20180510 import SetRefererConfigRequest

request = SetRefererConfigRequest.SetRefererConfigRequest()
request.set_DomainName('assets.yourdomain.com')
request.set_ReferType('block')
request.set_ReferList('yourdomain.com\nwww.yourdomain.com')
request.set_AllowEmpty('off')  # 禁止空Referer访问

client.do_action_with_exception(request)
```
