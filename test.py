import httpx
actions_url = 'http://miharpi:8000/bark/'
async def second_user(sound_file: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{actions_url}/{sound_file}')

