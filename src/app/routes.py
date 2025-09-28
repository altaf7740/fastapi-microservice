import sys

from fastapi import APIRouter

from core.config.logging import logger

router = APIRouter()


@router.get("/get-health")
async def health_check():
    logger.info('this is logger object for info')
    logger.debug('this is logger object for debug')
    logger.error('this is logger object for error')
    logger.critical('this is logger object for critical')
    logger.warning('this is logger object for warning')
    print('this is general print')
    print('this is stdout print', file=sys.stdout)
    print("this is std err print", file=sys.stderr)
    return {"message": "app is runnings"}
