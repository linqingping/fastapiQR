from fastapi import APIRouter,FastAPI, Form, File, UploadFile
from fastapi.responses import RedirectResponse,HTMLResponse
from starlette.requests import Request
from PIL import Image,ImageEnhance
import pyzbar.pyzbar as pyzbar
import io
import base64

router = APIRouter()


def home_html():
    html_content = """
<!DOCTYPE html>
<head>
<style type="text/css">
input[type="file"]{
   -webkit-appearance: none;
   text-align: left;
   -webkit-rtl-ordering:  left;
}
input[type="file"]::-webkit-file-upload-button{
   -webkit-appearance: none;
   float: right;
   margin: 0 0 0 10px;
   border: 1px solid #aaaaaa;
   border-radius: 4px;
   background-image: -webkit-gradient(linear, left bottom, left top, from(#d2d0d0), to(#f0f0f0));
   background-image: -moz-linear-gradient(90deg, #d2d0d0 0%, #f0f0f0 100%);
}
input[type=submit]{
 			width: 110px;
 			height: 40px;
            border-radius: 4px;
            border: 1px solid #aaaaaa;
 			background-color: rgb(0,201,87);
            # background-image: -webkit-gradient(linear, left bottom, left top, from(#d2d0d0), to(#f0f0f0));
            # background-image: -moz-linear-gradient(90deg, #d2d0d0 0%, #f0f0f0 100%);
 		}

</style>
</head>
<form method="post" action="/upload/" enctype="multipart/form-data">
<div style="text-align: center; width:100%;">
 <div style="margin: 5% 0 0 25%; width:50%; border-style: solid;  border-width: 1px; border-color: #98bf21;">
   <h1 style="text-align: center;">二维码在线识别</h1>
    <input type="file" id="file" name="file_obj" multiple></br>
    <input type="submit" value="二维码识别" style="color:white;font-weight:bolder">
 </div>
 </div>
</form>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/")
async def scan():
    return home_html()


# 渲染返回内容
def generate_html_response(contents,barcodeData):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fastapi Show Image</title>
</head>
<body>
   <div style="text-align: center; width:100%;">
      <img style="margin: 0 auto;" src='data:;base64,"""+contents.decode()+"""'>
      <h1 style="text-align: center;">二维码信息:<a href='"""+barcodeData+"""'>"""+barcodeData+"""</a></h1>
   </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)

#获取前端上传的文件
@router.post("/upload/")
async def upload(request: Request,
                # file: bytes = File(...),       # # 把文件对象转为bytes类型,这种类型的文件无法保存
                file_obj: UploadFile = File(...),    # UploadFile转为文件对象，可以保存文件到本地
                # info: str = Form(...)
                ):
    #读取文件
    contents = await file_obj.read()
    #转成字节流可以网页显示
    # print(base64.b64encode(contents))
    imgBuf = io.BytesIO(contents)
    #以 open() 方法打开了imgBuf图像，构建了名为 img 的实例
    img = Image.open(imgBuf)
    #使用 show() 方法来查看实例。注意，PIL 会将实例暂存为一个临时文件，而后打开它
    # print (img.name)
    # img = ImageEnhance.Brightness(img).enhance(2.0)#增加亮度
    # img = ImageEnhance.Sharpness(img).enhance(17.0)#锐利化
    # img = ImageEnhance.Contrast(img).enhance(4.0)#增加对比度
    img = img.convert('L')#灰度化
    img = img.convert("1")
    # img.show()
    barcodes = pyzbar.decode(img)
    # print(barcodes)
    # 读取二维码信息
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        # print(barcodeData)
    #返回响应页面    
    return generate_html_response(base64.b64encode(contents),barcodeData)
    
