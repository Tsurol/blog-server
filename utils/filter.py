from datetime import datetime

import timeago


def time_filter(dt):
    """日期和时间格式化显示"""
    # 3分钟前/1小时前
    # dt:datetime类型
    now = datetime.now()
    return timeago.format(dt, now, 'zh_CN')
