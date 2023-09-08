## 简介
提取并聚合chromego中的节点，并套上warp，让你感受白嫖加隐私的快乐体验
完全是面向chromego写的，所以很多地方都写死了
## 为什么要套上warp
首先chromego屏蔽了很多网站，包括你喜欢的p开头的网站，套上warp可以突破这一层限制。
第二我并不喜欢使用机场等服务，原因就是机场主或者节点主完全知道你访问的网站，虽然有一层https加密，但是他们还是可以知道你访问的域名已经你连接的时间，套上warp之后，他们只能看到一串加密流量。
第三，我为什么要提取节点出来，不仅仅是因为方便管理，可以在一个配置文件中切换不同的节点。而且是因为我并不喜欢使用他们所提供的客户端，虽然chromego所提供的客户端并没有什么问题，但是我还是喜欢自己常用的客户端。
## 不要用我配置文件中的warp
因为这是我自己的
可以用warp+机器人和提取wg节点替换掉配置文件中的wg信息
[warp提取wireguard网站](https://replit.com/@misaka-blog/wgcf-profile-generator)
[warp+机器人](https://t.me/generatewarpplusbot)
## clash-meta订阅链接(小火箭兼容，注意shadowtls可能无法使用需要手动添加host）
### 原始版本
```
https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/merged_warp_proxies.yaml
```
### 套上warp版本
```
https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/merged_proxies.yaml
```
## 加速的订阅链接
### 原始版本
```
https://fastly.jsdelivr.net/gh/vveg26/chromego_merge@main/sub/merged_proxies.yaml
```
### 套上warp版本
```
https://fastly.jsdelivr.net/gh/vveg26/chromego_merge@main/sub/merged_warp_proxies.yaml
```

## Chromego聚合说明
| ChromeGo文件夹 | 协议 | 结果 | 备注 |
|--------|--------|--------|--------|
| clash.meta   | reality vision  | 已聚合   |     | 
| hysteria   | hysteria1   | 已聚合   |     | 
| xray   | reality grpc tcp   | 已聚合   |     | 
| sing-box   | shadowtls  v1  | 已聚合   | clash-meta对v1的支持有问题导致并无法在clashmeta中使用，可以手动拿出节点放入小火箭使用，并且我不知道chromego为什么搞个v1版本，明明v2 v3早就出了    | 
| clashB v2go v2rayB   | 各种ss vmess   | 未聚合   |  又臭又长很多节点都已经失效   | 
| naiveproxy   | naiveproxy   | 未聚合   |  需要用它自己的客户端   | 
| psiphon   | 未知   | 未聚合   |  不知道是什么东西   | 
## 致谢
[chromego](https://github.com/bannedbook/fanqiang/tree/master/ChromeGo)
