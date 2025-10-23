from pydantic import BaseModel


class CustomerData(BaseModel):
    recency: int
    frequency: int
    monetary: float

    class Config:
        json_schema_extra = {
            "example": {
                "recency": 15,
                "frequency": 2,
                "monetary": 350.75
            }
        }


class SegmentResponse(BaseModel):
    segment_name: str
    cluster_label: int