import sys
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from utils.logger import logger
from config import Constants


def send_report(report):
    my_sender = 'LanceLiang2018@163.com'  # 发件人邮箱账号
    my_pass = '1352040930smtp'  # 发件人邮箱密码
    # my_user = '1352040930@qq.com'  # 收件人邮箱账号
    try:
        if type(report) is dict:
            report = json.dumps(report)
        msg = MIMEText(str(report), 'plain', 'utf-8')
        msg['From'] = formataddr(["GBK errors", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(['Dear Chiro', my_sender])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = f"chiblog v{Constants.VERSION}的新bug report"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_sender, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:
        logger.error('错误信息邮件发送失败！ %s' % e)


def form_report(e):
    report = {
        'string': str(e),
        'file': e.__traceback__.tb_frame.f_globals['__file__'],
        'line': e.__traceback__.tb_lineno
    }
    return report


def report_it(e):
    logger.error("产生了无法预知的错误")
    logger.error("错误内容如下:")
    error = form_report(e)
    logger.error(error['string'])
    logger.error('文件 %s' % error['file'])
    logger.error('行号 %s' % error['line'])
    logger.info('正在尝试反馈错误...')
    logger.info('尝试发送bug报告邮件...')
    send_report(error)
    logger.info('发送bug报告邮件成功')
    try:
        logger.info('尝试把bug发送到远程数据库...')
        from database.database import DataBase
        _db = DataBase()
        _db.error_report(error)
    except Exception as e2:
        logger.error('把bug发送到远程数据库失败')
        send_report(e2)
    logger.info('发送bug报告完成。')
    sys.exit(1)
