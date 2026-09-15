import json
import os
import urllib.parse
import urllib.request

def cors(body, status=200):
    return {
        "statusCode": status,
        "headers": {"Content-Type":"application/json","Cache-Control":"s-maxage=30, stale-while-revalidate=120"},
        "body": json.dumps(body)
    }

def query_supabase(table, params):
    url=os.environ["SUPABASE_URL"].rstrip("/")+"/rest/v1/"+table+"?"+urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={
        "apikey":os.environ["SUPABASE_ANON_KEY"],
        "Authorization":"Bearer "+os.environ["SUPABASE_ANON_KEY"],
    })
    with urllib.request.urlopen(req,timeout=8) as r:
        return json.loads(r.read().decode())

def handler(request):
    try:
        posts=query_supabase("posts",{
            "select":"id,title,content,category,image_url,message_url,published_at",
            "is_published":"eq.true",
            "order":"published_at.desc",
            "limit":"60"
        })
        channels=query_supabase("channels",{
            "select":"id,name,url,is_main,sort_order",
            "is_active":"eq.true",
            "order":"sort_order.asc"
        })
        return cors({"posts":posts,"channels":channels})
    except Exception as e:
        return cors({"error":"Database configuration or connection failed"},500)
