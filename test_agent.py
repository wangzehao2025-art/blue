# -*- coding: utf-8 -*-
"""测试 AI 选品顾问 Agent 完整流程

使用方法:
    1. 设置环境变量: export DEEPSEEK_API_KEY=sk-xxx
    2. 或者创建 .env 文件 (参考 .env.example)
    3. 运行: python test_agent.py
"""
import requests, json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 从环境变量读取 API Key (不要硬编码!)
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not API_KEY:
    print("❌ 请先设置环境变量 DEEPSEEK_API_KEY")
    print("   例如: export DEEPSEEK_API_KEY=sk-xxx")
    print("   或者创建 .env 文件 (参考 .env.example)")
    sys.exit(1)

BASE_URL = "https://api.deepseek.com/v1"

TOOLS = [
    {"type":"function","function":{
        "name":"search_opportunities",
        "description":"从内置 318+ 产品方向的机会库中筛选符合条件的产品。返回 TOP 20 结果。",
        "parameters":{"type":"object","properties":{
            "category":{"type":"string","description":"主类目: 宠物用品/家居收纳/厨房用品/清洁工具/数码配件/车载用品/母婴周边/服饰配件/运动户外/文具办公/礼品包装DIY/美妆个护工具"},
            "priceBand":{"type":"string"},"beginnerOnly":{"type":"boolean"},
            "lowRiskOnly":{"type":"boolean"},"excludeHighRisk":{"type":"boolean"},
            "shortVideoFriendly":{"type":"boolean"},"keyword":{"type":"string"}
        }}
    }},
    {"type":"function","function":{
        "name":"get_opportunity_detail",
        "description":"查询单个产品的完整信息",
        "parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}
    }},
    {"type":"function","function":{
        "name":"add_to_candidate","description":"加入候选池",
        "parameters":{"type":"object","properties":{"name":{"type":"string"},"priority":{"type":"integer"},"note":{"type":"string"}},"required":["name"]}
    }},
    {"type":"function","function":{
        "name":"compute_profit","description":"计算毛利、净利润、保本售价",
        "parameters":{"type":"object","properties":{"price":{"type":"number"},"cost":{"type":"number"},"shipping":{"type":"number"},"commission":{"type":"number"}},"required":["price","cost"]}
    }},
    {"type":"function","function":{
        "name":"detect_risk","description":"检测合规风险与敏感词",
        "parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}
    }},
    {"type":"function","function":{
        "name":"search_library","description":"搜索资料中心",
        "parameters":{"type":"object","properties":{"keyword":{"type":"string"}}}
    }},
    {"type":"function","function":{
        "name":"list_categories","description":"列出所有 12 个主类目",
        "parameters":{"type":"object","properties":{}}
    }},
]

def mock_tool(name, args):
    if name == "search_opportunities":
        return {"count":5,"results":[
            {"name":"猫抓板","category":"宠物用品","subCategory":"猫用品","priceBand":"20-49","score":73,"level":"B","isHighRisk":False,"beginnerFriendly":8,"shortVideoPotential":8,"complianceRisk":2,"riskTags":[],"reason":"需求稳定、低客单、低合规风险、适合短视频展示、有差异化空间","recommendedPlatforms":["抖音","淘宝","拼多多","小红书"],"differentiationIdeas":["造型差异化","组合套装","多猫家庭场景"]},
            {"name":"猫玩具球","category":"宠物用品","subCategory":"猫用品","priceBand":"0-19","score":71,"level":"B","isHighRisk":False,"beginnerFriendly":9,"shortVideoPotential":8,"complianceRisk":1,"riskTags":[],"reason":"超低客单+短视频友好+复购高","recommendedPlatforms":["抖音","拼多多"],"differentiationIdeas":["造型多样化"]},
            {"name":"宠物除毛刷","category":"宠物用品","subCategory":"通用宠物","priceBand":"0-19","score":70,"level":"B","isHighRisk":False,"beginnerFriendly":8,"shortVideoPotential":9,"complianceRisk":1,"riskTags":[],"reason":"刚需+短视频前后对比效果强","recommendedPlatforms":["抖音","小红书"],"differentiationIdeas":["前后对比卖点"]},
            {"name":"猫砂垫","category":"宠物用品","subCategory":"猫用品","priceBand":"20-49","score":72,"level":"B","isHighRisk":False,"beginnerFriendly":8,"shortVideoPotential":7,"complianceRisk":1,"riskTags":[],"reason":"高复购+刚需","recommendedPlatforms":["抖音","淘宝"],"differentiationIdeas":["颜色花纹"]},
            {"name":"狗狗胸背带","category":"宠物用品","subCategory":"狗用品","priceBand":"20-49","score":69,"level":"C","isHighRisk":False,"beginnerFriendly":7,"shortVideoPotential":7,"complianceRisk":2,"riskTags":[],"reason":"出行刚需,但同质化较高","recommendedPlatforms":["抖音"],"differentiationIdeas":["反光面料"]}
        ]}
    elif name == "get_opportunity_detail":
        return {"name":args.get("name"),"category":"宠物用品","subCategory":"猫用品","score":73,"level":"B","reason":"需求稳定","differentiationIdeas":["造型差异化","多猫家庭场景"],"recommendedPlatforms":["抖音","淘宝","拼多多"],"targetUsers":["新手养猫人群","多猫家庭","租房养猫人群"],"contentAngles":["猫咪真实使用","旧沙发被抓 vs 使用猫抓板"],"scores":{"需求稳定性":8,"竞争可切入性":6,"新手友好度":8,"内容种草能力":8,"差异化空间":7}}
    elif name == "compute_profit":
        price = float(args.get("price",0)); cost = float(args.get("cost",0))
        shipping = float(args.get("shipping",3)); commission = float(args.get("commission",5))/100
        gross = price - cost - shipping
        net = gross - price * commission - price*0.05 - 3
        return {"毛利":f"{gross:.2f} 元","毛利率":f"{gross/price*100:.1f}%","预估净利润":f"{net:.2f} 元","净利润率":f"{net/price*100:.1f}%","保本售价":f"{(cost+shipping+3)/(1-commission-0.05):.2f} 元","利润评级":"良好" if net/price>=0.25 else "可接受"}
    elif name == "detect_risk":
        return {"产品名":args.get("name"),"高风险类目":"无","宣传敏感词命中":"无","整体判断":"低风险,可继续验证","建议":"无明显风险,但仍需独立核验平台政策"}
    elif name == "search_library":
        return {"count":0,"results":[]}
    elif name == "add_to_candidate":
        return {"success":True,"message":f"已加入候选池: {args.get('name')} (优先级 {args.get('priority',3)})"}
    elif name == "list_categories":
        return [{"name":"宠物用品","productCount":62}]
    return {"error":"未知工具"}

SYSTEM = """你是「全类目蓝海选品作战系统」的 AI 选品顾问。专门帮助小卖家做电商选品决策。

# 工具调用纪律 (必须严格遵守)
## 严禁
- 严禁连续调 3 次以上工具不出文本回复
- 严禁对一个简单问题调用 5+ 个工具: 用户问"推荐 3 个产品"= 1 次 search_opportunities + 直接回答
- 严禁同时调用 search_library 和 search_opportunities — 优先用 search_opportunities
- 严禁对返回的每个产品都跑 detail/profit/risk

## 推荐模式
- 推荐产品类: 1 次 search_opportunities + 直接 Markdown 回复
- 单品深度: 1-3 次工具 (get_opportunity_detail + 可选 detect_risk/compute_profit)
- 利润计算: 1 次 compute_profit
- 候选池操作: 1 次 add_to_candidate

# 输出风格
- Markdown 表格 + 结论先行
- 给出 2-3 个可执行下一步动作 (加入候选池 / 查竞品 / 算利润)"""

def call_llm(messages):
    resp = requests.post(f"{BASE_URL}/chat/completions",
        headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"},
        json={"model":"deepseek-chat","messages":messages,"tools":TOOLS,"tool_choice":"auto","max_tokens":2000,"temperature":0.3},
        timeout=60)
    return resp.json()

def run_agent(user_msg, test_name):
    print(f"\n{'='*70}")
    print(f"测试: {test_name}")
    print(f"{'='*70}")
    print(f"USER: {user_msg}\n")
    messages = [{"role":"system","content":SYSTEM},{"role":"user","content":user_msg}]
    total_calls = 0
    for round_num in range(8):
        result = call_llm(messages)
        if "error" in result:
            print(f"API ERROR: {result}"); return
        msg = result["choices"][0]["message"]
        usage = result.get("usage",{})
        am = {"role":"assistant"}
        if msg.get("content"): am["content"] = msg["content"]
        if msg.get("tool_calls"): am["tool_calls"] = msg["tool_calls"]
        messages.append(am)
        print(f"-- Round {round_num+1} (tokens: {usage.get('total_tokens','?')}) --")
        if msg.get("content"):
            print(f"AI 文本:\n{msg['content']}\n")
        if msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                fn = tc["function"]["name"]
                args = json.loads(tc["function"]["arguments"])
                total_calls += 1
                print(f"  工具 #{total_calls}: {fn}({json.dumps(args,ensure_ascii=False)})")
                result_data = mock_tool(fn, args)
                preview = json.dumps(result_data,ensure_ascii=False)[:200]
                print(f"    结果: {preview}{'...' if len(preview)==200 else ''}")
                messages.append({"role":"tool","tool_call_id":tc["id"],"content":json.dumps(result_data,ensure_ascii=False)})
        else:
            print(f"OK 收敛 (共 {total_calls} 次工具调用)")
            return
    print(f"WARN 达到 8 轮上限 (共 {total_calls} 次工具调用)")

if __name__ == "__main__":
    run_agent("我想做宠物用品方向,推荐 3 个低风险的产品给我", "Test 1: 推荐宠物用品")
    run_agent("猫抓板这个产品能详细讲讲吗", "Test 2: 单品深度")
    run_agent("我打算卖猫抓板, 售价 39, 成本 8, 帮我算下利润", "Test 3: 利润计算")
    run_agent("帮我把猫抓板加入候选池", "Test 4: 候选池操作")
