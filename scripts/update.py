import json, urllib.request, urllib.parse, xml.etree.ElementTree as ET, datetime, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
queries=['全国大学生统计建模大赛 报名','全国大学生市场调查与分析大赛 报名','全国大学生数学建模竞赛 赛题','泰迪杯 数据挖掘 挑战赛','美国大学生数学建模竞赛 MCM ICM','数维杯 数学建模','亚太地区大学生数学建模竞赛','华数杯 数学建模','大学生 数据分析 实践赛']
items=[];fail=[]
for q in queries:
 try:
  url='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':q,'hl':'zh-CN','gl':'CN','ceid':'CN:zh-Hans'})
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=20) as r: xml=ET.fromstring(r.read())
  for it in xml.findall('./channel/item')[:7]:
   title=it.findtext('title','');link=it.findtext('link','');date=it.findtext('pubDate','');src=it.find('source')
   if title and link:items.append({'title':title,'url':link,'published':date,'publisher':src.text if src is not None else '', 'competition':q})
 except Exception as e:fail.append({'query':q,'error':str(e)[:120]})
p=root/'data/updates.json'
try:old=json.loads(p.read_text())
except:old={'items':[]}
if items:
 seen=set();unique=[]
 for x in items:
  if x['url'] not in seen:unique.append(x);seen.add(x['url'])
 data={'last_success_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':unique[:60],'failed_queries':fail,'note':'新闻搜索线索，未经官方核实'}
else:
 data=old;data['last_attempt_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();data['failed_queries']=fail
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('notices',len(items),'failed',len(fail))
