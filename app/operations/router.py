from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.operations.models import Operation
from app.operations.schemas import OperationCreate

operation_router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@operation_router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.type == operation_type)
        result = await session.execute(query)
        data = []

        for row in result:
            data.append({
                "id": row[0],
                "quantity": row[1],
                "figi": row[2],
                "instrument_type": row[3],
                "date": str(row[4]),
                "type": row[5]
            })

        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@operation_router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Operation).values(**new_operation.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

