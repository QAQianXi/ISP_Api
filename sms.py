# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_env.client import Client as EnvClient
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_darabonba_string.client import Client as StringClient
from alibabacloud_darabonba_time.client import Client as TimeClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> DysmsapiClient:
        """
        使用AK&SK初始化账号Client
        """
        config = open_api_models.Config()
        config.access_key_id = "" # 此处请填写您的AccessKey ID/AccessKey Secret。
        config.access_key_secret = ""
        return DysmsapiClient(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client(EnvClient.get_env('ACCESS_KEY_ID'), EnvClient.get_env('ACCESS_KEY_SECRET'))
        # 1.发送短信
        send_req = dysmsapi_models.SendSmsRequest(
            phone_numbers=args[0],
            sign_name=args[1],
            template_code=args[2],
            template_param=args[3]
        )
        send_resp = client.send_sms(send_req)
        code = send_resp.body.code
        if not UtilClient.equal_string(code, 'OK'):
            ConsoleClient.log(f'错误信息: {send_resp.body.message}')
            return
        biz_id = send_resp.body.biz_id
        # 2. 等待 10 秒后查询结果
        UtilClient.sleep(5000)
        # 3.查询结果
        phone_nums = StringClient.split(args[0], ',', -1)
        for phone_num in phone_nums:
            query_req = dysmsapi_models.QuerySendDetailsRequest(
                phone_number=UtilClient.assert_as_string(phone_num),
                biz_id=biz_id,
                send_date=TimeClient.format('yyyyMMdd'),
                page_size=10,
                current_page=1
            )
            query_resp = client.query_send_details(query_req)
            dtos = query_resp.body.sms_send_detail_dtos.sms_send_detail_dto
            # 打印结果
            for dto in dtos:
                if UtilClient.equal_string(f'{dto.send_status}', '3'):
                    ConsoleClient.log(f'{dto.phone_num} 发送成功，接收时间: {dto.receive_date}')
                elif UtilClient.equal_string(f'{dto.send_status}', '2'):
                    ConsoleClient.log(f'{dto.phone_num} 发送失败')
                else:
                    ConsoleClient.log(f'{dto.phone_num} 正在发送中...')

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client(EnvClient.get_env('ACCESS_KEY_ID'), EnvClient.get_env('ACCESS_KEY_SECRET'))
        # 1.发送短信
        send_req = dysmsapi_models.SendSmsRequest(
            phone_numbers=args[0],
            sign_name=args[1],
            template_code=args[2],
            template_param=args[3]
        )
        send_resp = await client.send_sms_async(send_req)
        code = send_resp.body.code
        if not UtilClient.equal_string(code, 'OK'):
            ConsoleClient.log(f'错误信息: {send_resp.body.message}')
            return
        biz_id = send_resp.body.biz_id
        # 2. 等待 10 秒后查询结果
        await UtilClient.sleep_async(10000)
        # 3.查询结果
        phone_nums = StringClient.split(args[0], ',', -1)
        for phone_num in phone_nums:
            query_req = dysmsapi_models.QuerySendDetailsRequest(
                phone_number=UtilClient.assert_as_string(phone_num),
                biz_id=biz_id,
                send_date=TimeClient.format('yyyyMMdd'),
                page_size=10,
                current_page=1
            )
            query_resp = await client.query_send_details_async(query_req)
            dtos = query_resp.body.sms_send_detail_dtos.sms_send_detail_dto
            # 打印结果
            for dto in dtos:
                if UtilClient.equal_string(f'{dto.send_status}', '3'):
                    ConsoleClient.log(f'{dto.phone_num} 发送成功，接收时间: {dto.receive_date}')
                elif UtilClient.equal_string(f'{dto.send_status}', '2'):
                    ConsoleClient.log(f'{dto.phone_num} 发送失败')
                else:
                    ConsoleClient.log(f'{dto.phone_num} 正在发送中...')


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
