import os.path

from settings import PATH

statics = os.path.join(PATH, "python_plugins/statics")


def at(user_id: int) -> str:
    return f"[CQ:at,qq={user_id}]"


def face(face_id: int) -> str:
    return f"[CQ:face,id={face_id}]"


def image(url: str, ID: int = 40000, subType: int = 0) -> str:
    """ id	    类型
        40000	普通
        40001	幻影
        40002	抖动
        40003	生日
        40004	爱你
        40005	征友

        flash 表示闪照, show 表示秀图

        subType:
        0	正常图片
        1	表情包, 在客户端会被分类到表情包图片并缩放显示
        2	热图
        3	斗图
        4	智图?
        7	贴图
        8	自拍
        9	贴图广告?
        10	有待测试
        13	热搜图
    """
    return f"[CQ:image,url={url},type=show,id={ID},subType={subType}]"


def imageByFile(fileName: str, ID: int = 40000, subType: int = 0) -> str:
    """ id	    类型
        40000	普通
        40001	幻影
        40002	抖动
        40003	生日
        40004	爱你
        40005	征友

        flash 表示闪照, show 表示秀图

        subType:
        0	正常图片
        1	表情包, 在客户端会被分类到表情包图片并缩放显示
        2	热图
        3	斗图
        4	智图?
        7	贴图
        8	自拍
        9	贴图广告?
        10	有待测试
        13	热搜图
    """
    return f"[CQ:image,file={os.path.join(statics, fileName)},type=show,id={ID},subType={subType}]"


def record(url: str, magic: bool = False) -> str:
    """
    magic:默认 0, 设置为 1 表示变声
    """
    return f"[CQ:record,url={url},magic={int(magic)}]"


def recordByFile(fileName: str, magic: bool = False) -> str:
    """
    magic:默认 0, 设置为 1 表示变声
    """
    return f"[CQ:record,file={fileName},magic={int(magic)}]"


def shareUrl(url: str, title: str) -> str:
    return f"[CQ:share,url={url},title={title}]"


def voice(msg: str) -> str:
    return f"[CQ:tts,text={msg}]"
