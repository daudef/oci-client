import asyncio
import pathlib

from oci_client import _client, _helpers, _services


def generate_request_method(service: str, method: _client.HttpMethod):
    return f"""\
def {service}_{method.name.lower()}(
    self,
    route: str,{'''
    body: _helpers.JsonValue | bytes,''' if method.has_body else ''}
    output_file: typing.BinaryIO | None = None,
):
    return self.request(
        service='{service}',
        method=_client.HttpMethod.{method.name},
        route=route,
        body={'body' if method.has_body else None},
        output_file=output_file,
    )
"""


def generate_request_methods(services: list[str]):
    return '\n\n'.join(
        '\n'.join(4 * ' ' + line for line in generate_request_method(service, method).splitlines())
        for service in services
        for method in _client.HttpMethod
    )


async def main():
    async with _helpers.make_http_client() as http_client:
        services = list((await _services.get_service_region_endpoint_map(http_client)).values)

    with (pathlib.Path(_client.__file__).parent / 'client.py').open(
        mode='w', encoding='utf-8'
    ) as client_file:
        client_file.write(
            f"""\
import dataclasses
import typing

from oci_client import _client, _helpers


@dataclasses.dataclass  # noqa: PLR0904
class Client(_client.Client):
{generate_request_methods(services)}
"""
        )


if __name__ == '__main__':
    asyncio.run(main())
