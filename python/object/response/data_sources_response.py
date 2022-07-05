from pydantic import BaseModel

from python.object.response.combined_data_sources import CombinedDataSources


class DataSourcesResponse(BaseModel):
    data: CombinedDataSources
