import yaml
import codecs
import json
import urllib.request
# 定义一个空列表用于存储合并后的代理配置
merged_proxies = []
# 获取clash文本中的内容
try:
    with open('./urls/clash_urls.txt', 'r') as file:
        urls = file.read().splitlines()

    # 遍历每个网址
    for url in urls:
        try:
            # 使用适当的方法从网址中获取内容，这里使用urllib库示例
            response = urllib.request.urlopen(url)
            data = response.read().decode('utf-8')

            # 解析YAML格式的内容
            content = yaml.safe_load(data)

            # 提取proxies部分并合并到merged_proxies中
            proxies = content.get('proxies', [])

            merged_proxies.extend(proxies)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")


# shadowtls singbox节点处理
# try:
#     with open("./urls/shadowtls_urls.txt", "r") as file:
#         urls = file.read().splitlines()

#     # 遍历每个网址
#     for index, url in enumerate(urls):
#         try:
#             # 使用适当的方法从网址中获取内容，这里使用urllib库示例
#             response = urllib.request.urlopen(url)
#             data = response.read().decode("utf-8")
#             json_data = json.loads(data)

#             # 提取所需字段
#             method = json_data["outbounds"][0]["method"]
#             password = json_data["outbounds"][0]["password"]
#             server = json_data["outbounds"][1]["server"]
#             server_port = json_data["outbounds"][1]["server_port"]
#             server_name = json_data["outbounds"][1]["tls"]["server_name"]
#             name = f"shadowtls{index}"
#             # 创建当前网址的proxy字典
#             proxy = {
#                 "name": name,
#                 "type": "ss",
#                 "server": server,
#                 "port": server_port,
#                 "cipher": method,
#                 "password": password,
#                 "plugin": "shadow-tls",
#                 "client-fingerprint": "chrome",
#                 "plugin-opts": {
#                     "host": server_name,
#                     "password": "",
#                     "version": 1
#                 }
#             }

#             # 将当前proxy字典添加到所有proxies列表中
#             merged_proxies.append(proxy)
#         except Exception as e:
#             print(f"Error processing URL {url}: {e}")
# except Exception as e:
#     print(f"Error reading file: {e}")
#歇斯底里节点 json处理
try:
    with open("./urls/hysteria_urls.txt", "r") as file:
        urls = file.read().splitlines()

    # 遍历每个网址
    for index, url in enumerate(urls):
        try:
            # 使用适当的方法从网址中获取内容，这里使用urllib库示例
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            json_data = json.loads(data)

            # 提取所需字段
            auth = json_data["auth_str"]
            server_ports = json_data["server"]
            server_ports_slt = server_ports.split(":")
            server = server_ports_slt[0]
            ports = server_ports_slt[1]
            ports_slt = ports.split(",")
            server_port = int(ports_slt[0])
            if len(ports_slt) > 1:
                mport = ports_slt[1]
            else:
                mport = server_port
            

            server_name = json_data["server_name"]
            alpn = json_data["alpn"]
            protocol = json_data["protocol"]
            name = f"hysteria{index}"

            # 创建当前网址的proxy字典
            proxy = {
                "name": name,
                "type": "hysteria",
                "server": server,
                "port": server_port,
                "ports": mport,
                "auth_str": auth,
                "up": 11,
                "down": 55,
                "fast-open": True,
                "protocol": protocol,
                "sni": server_name,
                "skip-cert-verify": True,
                "alpn": [alpn]
            }

            # 将当前proxy字典添加到所有proxies列表中
            merged_proxies.append(proxy)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")


# xray json reality节点处理
try:
    with open("./urls/reality_urls.txt", "r") as file:
        urls = file.read().splitlines()

    # 遍历每个网址
    for index, url in enumerate(urls):
        try:
            # 使用适当的方法从网址中获取内容，这里使用urllib库示例
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            json_data = json.loads(data)

            # 提取所需字段
            protocol = json_data["outbounds"][0]["protocol"]
            server = json_data["outbounds"][0]["settings"]["vnext"][0]["address"]
            port = json_data["outbounds"][0]["settings"]["vnext"][0]["port"]
            uuid = json_data["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"]
            istls = True
            flow = json_data["outbounds"][0]["settings"]["vnext"][0]["users"][0]["flow"]
            # 传输方式
            network = json_data["outbounds"][0]["streamSettings"]["network"]
            publicKey = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["publicKey"]
            shortId = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["shortId"]
            serverName = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["serverName"]
            fingerprint = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["fingerprint"]
            # udp转发
            isudp = True
            name = f"reality{index}"
            
            # 根据network判断tcp
            if network == "tcp":
                proxy = {
                    "name": name,
                    "type": protocol,
                    "server": server,
                    "port": port,
                    "uuid": uuid,
                    "network": network,
                    "tls": istls,
                    "udp": isudp,
                    "flow": flow,
                    "client-fingerprint": fingerprint,
                    "servername": serverName,                
                    "reality-opts":{
                        "public-key": publicKey,
                        "short-id": shortId}
                }
                
            # 根据network判断grpc
            elif network == "grpc":
                serviceName = json_data["outbounds"][0]["streamSettings"]["grpcSettings"]["serviceName"]
                
                # 创建当前网址的proxy字典
                proxy = {
                    "name": name,
                    "type": protocol,
                    "server": server,
                    "port": port,
                    "uuid": uuid,
                    "network": network,
                    "tls": istls,
                    "udp": isudp,
                    "flow": flow,
                    "client-fingerprint": fingerprint,
                    "servername": serverName,
                    "grpc-opts":{
                        "grpc-service-name": serviceName
                    },
                    "reality-opts":{
                        "public-key": publicKey,
                        "short-id": shortId}
                }
            else:
                print(f"其他协议还未支持 URL {url}")
                proxy={}
                continue
            
            # 将当前proxy字典添加到所有proxies列表中
            merged_proxies.append(proxy)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")



# 读取普通的配置文件内容
with codecs.open('./templates/clash_template.yaml', 'r', encoding='utf-8') as file:
    config_data = yaml.safe_load(file)

# 读取warp配置文件内容
with codecs.open('./templates/clash_warp_template.yaml', 'r', encoding='utf-8') as file:
    config_warp_data = yaml.safe_load(file)

# 添加合并后的代理到proxies部分
config_data['proxies'].extend(merged_proxies)
config_warp_data['proxies'].extend(merged_proxies)
# 更新自动选择和节点选择的proxies的name部分
for group in config_data['proxy-groups']:
    if group['name'] == '自动选择' or group['name'] == '节点选择':
        group['proxies'].extend(proxy['name'] for proxy in merged_proxies)

for group in config_warp_data['proxy-groups']:
    if group['name'] == '自动选择' or group['name'] == '手动选择' or group['name'] == '负载均衡':
        group['proxies'].extend(proxy['name'] for proxy in merged_proxies)

# 将更新后的数据写入到一个YAML文件中，并指定编码格式为UTF-8
with codecs.open('./sub/merged_proxies.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config_data, file, sort_keys=False, allow_unicode=True)
with codecs.open('./sub/merged_warp_proxies.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config_warp_data, file, sort_keys=False, allow_unicode=True)
print("聚合成狗")
