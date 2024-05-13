from src.api.api_controller import ApiController

API = ApiController.get_instance()

async def ping() -> bool:
    response = await API.get(endpoint_path=[""])
    return response.status == 200