import base64
import json
import urllib.request
import yaml
import codecs

merged_proxies = []

try:
    with open("./urls/naiverproxy_urls.txt", "r") as file:
        urls = file.read().splitlines()

    # 遍历每个网址
    for index, url in enumerate(urls):
        try:
            # 使用适当的方法从网址中获取内容，这里使用urllib库示例
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            json_data = json.loads(data)
            proxy_str = json_data["proxy"]
            # 对 proxy 进行 Base64 编码
            encoded_proxy = base64.b64encode(proxy_str.encode()).decode()
            # 添加前缀
            naiveproxy = "http2://" + encoded_proxy
            merged_proxies.append(naiveproxy)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")



try:
    with open("./urls/shadowtls_urls.txt", "r") as file:
        urls = file.read().splitlines()

    # 遍历每个网址
    for index, url in enumerate(urls):
        try:
            # 使用适当的方法从网址中获取内容，这里使用urllib库示例
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            # 解析JSON数据
            json_data = json.loads(data)


            server = json_data["outbounds"][1]["server"]
            server_port = json_data["outbounds"][1]["server_port"]
            method = json_data["outbounds"][0]["method"]
            password = json_data["outbounds"][0]["password"]
            version = "1"
            host = json_data["outbounds"][1]["tls"]["server_name"]
            ss = f"{method}:{password}@{server}:{server_port}"
            shadowtls = f'{{"version": "{version}", "host": "{host}"}}'
            shadowtls_proxy = "ss://"+base64.b64encode(ss.encode()).decode()+"?shadow-tls="+base64.b64encode(shadowtls.encode()).decode()+f"#shadowtls{index}"
            
            merged_proxies.append(shadowtls_proxy)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")


try:
    with open("./urls/hysteria_urls.txt", "r") as file:
        urls = file.read().splitlines()

    # 遍历每个网址
    for index, url in enumerate(urls):
        try:
            # 使用适当的方法从网址中获取内容，这里使用urllib库示例
            response = urllib.request.urlopen(url)
            data = response.read().decode("utf-8")
            # 解析JSON数据
            json_data = json.loads(data)

            # 提取字段值
            server = json_data["server"]
            protocol = json_data["protocol"]
            up_mbps = json_data["up_mbps"]
            down_mbps = json_data["down_mbps"]
            alpn = json_data["alpn"]
            obfs = json_data["obfs"]
            insecure = int(json_data["insecure"])
            server_name = json_data["server_name"]
            fast_open = int(json_data["fast_open"])
            auth = json_data["auth_str"]
            # 生成URL
            hysteria = f"hysteria://{server}?peer={server_name}&auth={auth}&insecure={insecure}&upmbps={up_mbps}&downmbps={down_mbps}&alpn={alpn}&obfs={obfs}&protocol={protocol}&fastopen={fast_open}#hysteria{index}"
            merged_proxies.append(hysteria)
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
            spx = json_data["outbounds"][0]["streamSettings"]["realitySettings"]["spiderX"]
            # udp转发
            isudp = True
            name = f"reality{index}"
            
            # 根据network判断tcp
            if network == "tcp":
                reality = f"vless://{uuid}@{server}:{port}?security=reality&flow={flow}&type={network}&fp={fingerprint}&pbk={publicKey}&sni={serverName}&spx={spx}&sid={shortId}#REALITY{index}"

            # 根据network判断grpc
            elif network == "grpc":
                serviceName = json_data["outbounds"][0]["streamSettings"]["grpcSettings"]["serviceName"]
                reality = f"vless://{uuid}@{server}:{port}?security=reality&flow={flow}&&type={network}&fp={fingerprint}&pbk={publicKey}&sni={serverName}&spx={spx}&sid={shortId}&serviceName={serviceName}#REALITY{index}"
            else:
                print(f"其他协议还未支持 URL {url}")
                reality = ""
                continue
            
            # 将当前proxy字典添加到所有proxies列表中
            merged_proxies.append(reality)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")


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

            for proxy in proxies:
                server = proxy['server']
                port  = proxy['port']
                udp = proxy['udp']
                uuid = proxy['uuid']
                tls = proxy['tls']
                serverName = proxy['servername']
                flow = proxy['flow']
                network = proxy['network']
                publicKey = proxy['reality-opts']['public-key']
                fp = proxy['client-fingerprint']
                reality_meta =  f"vless://{uuid}@{server}:{port}?security=reality&flow={flow}&type={network}&fp={fingerprint}&pbk={publicKey}&sni={serverName}#reality_meta{index}"
                merged_proxies.append(reality_meta)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
except Exception as e:
    print(f"Error reading file: {e}")

# 将结果写入文件
try:
    with open("./sub/shadowrocket.txt", "w") as file:
        for proxy in merged_proxies:
            file.write(proxy + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")


try:
    with open("./sub/shadowrocket.txt", "r") as file:
        content = file.read()
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    with open("./sub/shadowrocket_base64.txt", "w") as encoded_file:
        encoded_file.write(encoded_content)
        
    print("Content successfully encoded and written to file.")
except Exception as e:
    print(f"Error encoding file content: {e}")
