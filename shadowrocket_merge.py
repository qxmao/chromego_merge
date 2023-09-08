import base64
import json
import urllib.request

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



# 将结果写入文件
try:
    with open("./sub/shadowrocket.txt", "w") as file:
        for proxy in merged_proxies:
            file.write(proxy + "\n")
except Exception as e:
    print(f"Error writing to file: {e}")