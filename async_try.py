import csv
import aiohttp
import asyncio
import ssl

collection_details = {
    # "pudgy penguins": {"base_url": "https://api.raritysniper.com/public/collection/pudgy-penguins/id/", "start_id": 1, "end_id": 8888},
    "gotcha gatcha": {"base_url": "https://api.raritysniper.com/public/collection/gotcha-gatcha/id/", "start_id": 1, "end_id": 998},
    "Rare ghost club":{"base_url":'https://api.raritysniper.com/public/collection/rare-ghost-club/id/', "start_id": 1, "end_id":5000},
    "robofrens":{"base_url":'https://api.raritysniper.com/public/collection/robofrens/id/', "start_id": 1, "end_id": 777},
    "bearsontheblock":{"base_url":'https://api.raritysniper.com/public/collection/bearsontheblock/id/', "start_id": 1, "end_id": 9496},
    "antvasion":{"base_url":'https://api.raritysniper.com/public/collection/antvasion/id/', "start_id": 1, "end_id": 477},
    "neon-pantheon-genesis":{"base_url":'https://api.raritysniper.com/public/collection/neon-pantheon-genesis/id/', "start_id": 1, "end_id": 838},
    "metagreys-v-2":{"base_url":'https://api.raritysniper.com/public/collection/metagreys-v-2/id/', "start_id": 1, "end_id": 136},
    "renderpunks":{"base_url":'https://api.raritysniper.com/public/collection/renderpunks/id/', "start_id": 1, "end_id": 997},
    "nft-worlds-genesis-avatars":{"base_url":'https://api.raritysniper.com/public/collection/nft-worlds-genesis-avatars/id/', "start_id": 1, "end_id": 11885},
    "dorkis":{"base_url":'https://api.raritysniper.com/public/collection/dorkis/id/', "start_id": 1, "end_id": 4724},
    "h8rschix":{"base_url":'https://api.raritysniper.com/public/collection/h8rschix/id/', "start_id": 1, "end_id": 9455},
    "noobs":{"base_url":'https://api.raritysniper.com/public/collection/noobs/id/', "start_id": 1, "end_id": 9999},
    "fury-of-the-fur":{"base_url":'https://api.raritysniper.com/public/collection/fury-of-the-fur/id/', "start_id": 1, "end_id": 9671},
   
 
    # Add more collections as needed
}

async def retrieve_nft_data(session, url):
    """
    Retrieve NFT information from the provided API URL.
    """
    try:
        # Disable SSL certificate verification
        ssl_context = ssl.SSLContext()
        async with session.get(url, ssl=ssl_context) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f'Failed to retrieve data from API ({url}): {e}')
        return None

async def display_rarity_rank(sem, collection_slug, nft_id, session, writer):
    """
    Retrieve rarity rank for the given NFT ID in the specified collection.
    """
    base_url = collection_details[collection_slug]["base_url"]
    url = f'{base_url}{nft_id}'
    async with sem:
        data = await retrieve_nft_data(session, url)
        if data:
            writer.writerow([collection_slug, nft_id, data.get('rank', 'N/A')])
        else:
            writer.writerow([collection_slug, nft_id, 'Failed'])

async def main():
    concurrency_limit = 2 
    sem = asyncio.Semaphore(concurrency_limit)

    async with aiohttp.ClientSession() as session:
        with open("rarity_details_async_try_22_5.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Collection Slug", "NFT ID", "Rarity Rank"])

            tasks = []
            for collection_slug, details in collection_details.items():
                start_id = details["start_id"]
                end_id = details["end_id"]
                for nft_id in range(start_id, end_id + 1):
                    task = display_rarity_rank(sem, collection_slug, nft_id, session, writer)
                    tasks.append(task)

            await asyncio.gather(*tasks)

        print("Details saved to rarity_details_async_try_22_5.csv")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print("An event loop is already running. Please run this script in an environment without an active event loop.")
    else:
        asyncio.run(main())
