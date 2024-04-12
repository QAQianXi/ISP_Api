import azure.functions as func
import logging
import sms
import json
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="fc_SendSMS", auth_level=func.AuthLevel.ANONYMOUS)
def fc_SendSMS(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 尝试从查询字符串或请求体中获取参数
    try:
        phone_numbers = req.params.get("phone_numbers") or req.get_json().get('phone_numbers')
        sign_name = req.params.get("sign_name") or req.get_json().get('sign_name')
        template_code = req.params.get("template_code") or req.get_json().get('template_code')
        template_param = req.params.get("template_param") or req.get_json().get('template_param')
    except ValueError:
        # 如果JSON解析失败，则参数仍然可能为空
        phone_numbers = sign_name = template_code = template_param = None

    # 检查所有必要参数是否都已提供
    if not all([phone_numbers, sign_name, template_code, template_param]):
        missing_params = ["phone_numbers", "sign_name", "template_code", "template_param"]
        provided_params = [phone_numbers is not None, sign_name is not None, template_code is not None, template_param is not None]
        missing = [param for param, provided in zip(missing_params, provided_params) if not provided]
        
        error_message = {
            "error": "缺少必要参数",
            "missing_parameters": missing
        }
        return func.HttpResponse(body=json.dumps(error_message, ensure_ascii=False),
                                 status_code=400,
                                 headers={"Content-Type": "application/json"})

    # 如果所有参数都有效，则处理请求
    print(f"[{phone_numbers},{sign_name},{template_code},{template_param}]")
    sms.Sample.main([phone_numbers, sign_name, template_code, template_param])
    return func.HttpResponse(f"[{phone_numbers},{sign_name},{template_code},{template_param}短信已尝试发送]")

@app.route(route="fc_CreatAlarm_YOLO", auth_level=func.AuthLevel.ANONYMOUS)
def fc_CreatAlarm_YOLO(req: func.HttpRequest) -> func.HttpResponse:
    
    image_base64 = req.params.get('image_base64') or req.get_json().get('image_base64', '')
    alarm_time = req.params.get('alarm_time') or req.get_json().get('alarm_time', '')
    device_id = req.params.get('device_id') or req.get_json().get('device_id', '')
    alarm_name = req.params.get('alarm_name') or req.get_json().get('alarm_name', '')
    device_latitude = req.params.get('device_latitude') or req.get_json().get('device_latitude', '')
    device_longitude = req.params.get('device_longitude') or req.get_json().get('device_longitude', '')

    # 检查所有必要参数是否都已提供
    missing_params = []
    if not alarm_time:
        missing_params.append('alarm_time')
    if not device_id:
        missing_params.append('device_id')
    if not alarm_name:
        missing_params.append('alarm_name')

    # 如果有缺失的参数，返回错误响应
    if missing_params:
        error_message = {
            "error": "Missing required parameters",
            "missing_parameters": missing_params
        }
        return func.HttpResponse(body=json.dumps(error_message, ensure_ascii=False),
                                 status_code=400,
                                 headers={"Content-Type": "application/json"})

    # 获取图片连接
    response_img={}
    if image_base64 != "":
        url = "https://uapis.cn/api/baseimg.php"
        payload = {'imageData': image_base64}
        files = [
        ]
        headers = {}
        response_img = requests.request("POST", url, headers=headers, data=payload, files=files)
        # data = json.load(response.json())
        response_img = response_img.json()
        print(response_img["img"])

    # 获取地址
    alarm_location = ""
    if device_longitude != "":
        url = f"https://restapi.amap.com/v3/geocode/regeo?location={device_longitude},{device_latitude}&key=68b87608ab54a51b6ddc402689bc5495"
        payload = {}
        headers = {}
        response_loc = requests.request("GET", url, headers=headers, data=payload)
        response_loc = response_loc.json()
        print(response_loc["regeocode"]["formatted_address"])
        alarm_location = response_loc["regeocode"]["formatted_address"]
        
        
        

    result = {"img": response_img.get("img",""), "alarm_time": alarm_time, 'device_id': device_id, "alarm_name": alarm_name,
              "alarm_location": alarm_location, "device_latitude": device_latitude,
              "device_longitude": device_longitude,"alarm_labels":"警告","device_status":"open"}
    headers = {"content-type":"application/json"}
    azure_url = "https://prod-51.southeastasia.logic.azure.com:443/workflows/1ada9a5acf494e7899da177c38de89c5/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=-R7_nyif9R92W13TaR4G9vq6bK8cnbdceH9SdCVHxUY"
    result_azure = requests.request("POST", azure_url, headers=headers, data=json.dumps(result))
        # return func.HttpResponse({img:response_data["img"]})
    print(result_azure.text)
    return func.HttpResponse(status_code=200, headers={"Content-Type": "application/json"})