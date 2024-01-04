import asyncio

from oci_client import _helpers, _services


async def main():
    async with _helpers.make_http_client() as http_client:
        _services.set_bundled_service_region_endpoint_map(
            await _services.get_service_region_endpoint_map(http_client)
        )


if __name__ == '__main__':
    asyncio.run(main())
