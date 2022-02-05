import http

import pytest

pytestmark = pytest.mark.asyncio


async def test_role_list_and_detail(make_request, access_token):
    """Check role's detail & list methods"""
    """ List"""
    response_list = await make_request(
        endpoint="/role/", http_method="get", headers=access_token
    )
    assert response_list.status == http.HTTPStatus.OK
    """ Detail """
    role_id: str = response_list.body.get("data")[0].get("roles")[0].get("id")
    response_detail = await make_request(
        endpoint="/role/", http_method="get", headers=access_token, params=role_id
    )
    assert response_detail.status == http.HTTPStatus.OK


# async def test_role_create(make_request, access_token):
#     test_role: str = "test_role"
#     response = await make_request(
#         endpoint="/role/",
#         http_method="delete",
#         headers=access_token,
#         data={"name": test_role},
#     )
#     response_name: str = response.body.get("data")[0].get("name")
#     assert response.status == http.HTTPStatus.CREATED
#     assert response_name == test_role


# async def test_role_create(make_request, access_token):
#     test_role: str = "test_role"
#     response = await make_request(
#         endpoint="/role/", http_method="post", headers=access_token,
#         data={"name": test_role}
#     )
#     response_name: str = response.body.get("data")[0].get("name")
#     assert response.status == http.HTTPStatus.CREATED
#     assert response_name == test_role
