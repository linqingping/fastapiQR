from fastapi import APIRouter
#使用配置
import sys
sys.path.append('..')
from conf.settings import *

router = APIRouter()

@router.get("/get")
async def sey_hello():
    return "hello"

@router.post("/post")
async def sey_hello():
    return "hello"




#--------------------------------------------------->
#判断内网IP
def ip_into_int(ip):
    from functools import reduce
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))
 
def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c


from pydantic import BaseModel
class IP(BaseModel):
    value: str

@router.post("/IPType")
async def ip_type(ip:IP):
    result=is_internal_ip(ip.value)
    if result:
        return "is internal IP"
    return "is public IP"    
#--------------------------------------------------<



# responses = {
#     404: {"description": "Item not found"},
#     302: {"description": "The item was moved"},
#     403: {"description": "Not enough privileges"},
#     422: {"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}}},
# }
#https://www.cnblogs.com/mazhiyong/p/13298832.html, FastAPI 高级定制的Response 
@router.get("/mysql/conf",responses={
    200:{
            "description": "return mysql info",
            "content": {
                "application/json": {
                    "example": {"host": "127.0.0.1", "user": "root","port":"3306","passwd":"123456"}
                }
            }
        }
    })
async def mysql_conf():
    return {"host":host,"user":user,"port":port,"passwd":passwd}

# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: int = Path(..., title="The ID of the item to get", ge=1),
#     q: Optional[str] = Query(None, alias="item-query"),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
# @app.get("/items/{item_id}")
# @app.post("/items/{item_id}")
# async def read_item(request: Request,item_id: str, q: Optional[str] = None, short: bool = False):
#     if request.method == "POST":
#         return "POST" 
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item
