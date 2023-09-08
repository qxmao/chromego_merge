import yaml
import codecs
import json
# 定义一个空列表用于存储合并后的代理配置
merged_proxies = []

# 从reality文本文件中读取网址
with open('./urls/clash_urls.txt', 'r') as file:
    urls = file.read().splitlines()

# 遍历每个网址
for url in urls:
    # 使用适当的方法从网址中获取内容，这里使用urllib库示例
    import urllib.request
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')

    # 解析YAML格式的内容
    content = yaml.safe_load(data)

    # 提取proxies部分并合并到merged_proxies中
    proxies = content.get('proxies', [])
    merged_proxies.extend(proxies)


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