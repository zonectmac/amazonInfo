# -*- coding: utf-8 -*-

'''
发送邮件
'''

import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os.path
import email
import mimetypes
import os
from os.path import getsize
import traceback


class EmailManager:
    '''
    send email to the given email address automatically
    '''

    def __init__(self, **kw):
        ' 构造函数 '
        self.kw = kw

        # self.smtp_server = "smtp.exmail.qq.com"
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10M

    def run(self):
        # 总入口
        try:
            # 初始化
            self.__my_init()
            # 登录SMTP服务器，验证授权
            server = self.get_login_server()
            # 生成邮件主体内容
            main_msg = self.get_main_msg()
            # 生成邮件附件内容
            file_msg = self.get_attach_file_msg()

            if file_msg is not None:
                main_msg.attach(file_msg)

            # 得到格式化后的完整文本
            fullText = main_msg.as_string()

            # 发送邮件
            server.sendmail(self.msg_from, self.receiver, fullText)
        except Exception as e:
            print(e)
            exstr = traceback.format_exc()
            print(exstr)
            server.quit()
            exit()

    def get_main_msg(self):
        ' 生成邮件主体内容 '
        # 构造MIMEMultipart对象做为根容器
        main_msg = MIMEMultipart()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        text_msg = MIMEText(self.msg_content, _charset="utf-8")
        main_msg.attach(text_msg)

        # 设置根容器属性
        main_msg['From'] = self.msg_from
        main_msg['To'] = self.msg_to
        main_msg['Cc'] = self.msg_cc
        main_msg['Subject'] = self.msg_subject
        main_msg['Date'] = self.msg_date

        return main_msg

    def get_attach_file_msg(self):
        ' 生成邮件附件内容 '
        if self.attach_file is not None and self.attach_file != "":
            try:
                self.validate_file_size()

                data = open(self.attach_file, 'rb')
                ctype, encoding = mimetypes.guess_type(self.attach_file)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                file_msg = MIMEBase(maintype, subtype)
                file_msg.set_payload(data.read())
                data.close()

                email.encoders.encode_base64(file_msg)  # 把附件编码

                ## 设置附件头
                basename = os.path.basename(self.attach_file)
                file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头

                return file_msg
            except Exception as e:
                print(e)
                return None

        else:
            return None

    def get_login_server(self):
        ' 登录SMTP服务器，验证授权信息 '
        server = smtplib.SMTP(self.smtp_server)
        server.login(self.server_username, self.server_pwd)  # 仅smtp服务器需要验证时

        return server

    def validate_file_size(self):
        ' 验证文件大小是否合法 '
        if getsize(self.attach_file) > self.MAX_FILE_SIZE:
            raise Exception(u'附件过大，上传失败')

    def __my_init(self):
        ' 配置初始化 '
        # 邮箱登录设置
        self.smtp_server = self.__get_cfg('smtp_server')
        self.server_username = self.__get_cfg('server_username')
        self.server_pwd = self.__get_cfg('server_pwd')

        # 邮件内容设置
        self.receiver = self.__get_cfg('msg_to')+self.__get_cfg('msg_cc')

        self.msg_from = self.server_username
        self.msg_to = ','.join(self.__get_cfg('msg_to'))
        self.msg_cc = ','.join(self.__get_cfg('msg_cc'))
        self.msg_subject = self.__get_cfg('msg_subject')
        self.msg_date = self.__get_cfg('msg_date')
        print(self.msg_date)
        self.msg_content = self.__get_cfg('msg_content')

        # 附件
        self.attach_file = self.__get_cfg('attach_file', throw=False)

    def __get_cfg(self, key, throw=True):
        ' 根据key从**kw中取得相应的配置内容 '
        cfg = self.kw.get(key)
        if throw == True and (cfg is None or cfg == ''):
            strmsg = "配置不能为空！"
            msg = strmsg.encode('utf-8')
            raise Exception(msg.decode('utf-8', 'strict'))

        return cfg
