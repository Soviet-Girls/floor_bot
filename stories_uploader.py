from typing import TYPE_CHECKING, List, Union
from vkbottle.tools import BaseUploader

if TYPE_CHECKING:
    from vkbottle.tools.dev.uploader.base import Bytes

class StoriesUploader(BaseUploader):
    NAME = "picture.png"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME
    
    async def get_server(self, **kwargs) -> dict:
        return (await self.api.request("stories.getPhotoUploadServer", kwargs))["response"]
    
    async def upload(self, file_source: Union[str, "Bytes"], **params) -> Union[str, List[dict]]:
        server = await self.get_server(**params)
        print(server)
        data = await self.read(file_source)
        print(data)
        file = self.get_bytes_io(data)
        print(file)
        
        uploader = await self.upload_files(server["upload_url"], {"file": file})
        print(uploader)
        if not uploader:
            raise ValueError("Failed to upload the file")
        return (await self.api.request("stories.save", uploader))["response"]