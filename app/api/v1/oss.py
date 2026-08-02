import alibabacloud_oss_v2 as oss
from fastapi import APIRouter
from datetime import timedelta
import os
# 加载环境变量
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

# OSS 域名配置
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
OSS_BUCKET = os.getenv("OSS_BUCKET")

_oss_client = None


def _get_oss_client():
    """懒加载 OSS 客户端，避免导入时就要求凭证"""
    global _oss_client
    if _oss_client is None:
        credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = 'cn-beijing'
        _oss_client = oss.Client(cfg)
    return _oss_client


@router.get("/oss/presign")
def presign_upload(filename: str):
    # 根据文件扩展名判断 Content-Type
    content_type_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    ext = filename.split(".")[-1].lower() if "." in filename else "jpg"
    content_type = content_type_map.get(ext, "application/octet-stream")

    pre_result = _get_oss_client().presign(oss.PutObjectRequest(
        bucket=OSS_BUCKET,
        key=filename,
        content_type=content_type,
    ), expires=timedelta(seconds=3600))

    # 返回上传 URL 和可访问的图片路径
    return {
        "uploadUrl": pre_result.url.strip('"'),
        "contentType": content_type,
        "accessUrl": f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{filename}"
    }
