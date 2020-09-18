import uvicorn
from typing import Optional
from fastapi import FastAPI,Request,Path,Query
# from conf.settings import *
#跨域
from fastapi.middleware.cors import CORSMiddleware
#导入路由
from routers import upload

app = FastAPI(title="二维码扫描API",description="二维码扫描")
#支持仅限于支持哪些域名进行跨域
# origins = [
#     "http://localhost",
#     "http://localhost:8000",
# ]
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#添加router
#app.include_router(hello.router,prefix="/test")
#app.include_router(home.router)
app.include_router(upload.router)
# print(host)

#uvicorn main:app --reload --host=0.0.0.0
# 添加后命令行直接执行python main.py  
if __name__ == '__main__':
     uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, debug=True)



