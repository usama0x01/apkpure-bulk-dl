import asyncio
import aiohttp
from tqdm import tqdm
from fake_useragent import UserAgent

async def download_package(package_name, pbar):
    url = f"https://d.apkpure.com/b/APK/{package_name}?version=latest"
    headers = {'User-Agent': UserAgent().random}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True, headers=headers) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(f"{package_name}.apk", "wb") as f:
                        f.write(content)
                else:
                    print(f"Failed to download: {package_name}")
    except aiohttp.ClientError as e:
        print(f"Error downloading {package_name}: {e}")

    pbar.update(1)

async def main():
    with open("package_list.txt", "r") as file:
        package_names = [line.strip() for line in file]

    # Create the progress bar
    with tqdm(total=len(package_names), desc="Downloading packages", unit="pkg") as pbar:
        tasks = [download_package(package_name, pbar) for package_name in package_names]

        # Execute the tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
