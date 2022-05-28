from requests import get, patch
import os

domain = os.environ.get("SITE_ADDRESS")
foobar = "foobar@bingbong.com"
barfoo = "barfoo@bingbong.com"
admin_auth_header = {"authorization": os.environ.get("TEST_ADMIN_TOKEN")}
user_auth_header = {"authorization": os.environ.get("TEST_USER_TOKEN")}

test_auth_get_investments_user_role = get(f"{domain}/user/{barfoo}/investments", headers=user_auth_header)

if test_auth_get_investments_user_role.status_code == 200:
    print("(1/4) User Role Test: read:investments \n PASSED (200)\n")
else:
    print(f"(1/4) User Role Test: read:investments \n FAILED ({test_auth_get_investments_user_role.status_code})\n")

test_auth_give_bonus_user_role = patch(f"{domain}/user/{barfoo}", json=dict(bonus=float(50000)), headers=user_auth_header)

if test_auth_give_bonus_user_role.status_code == 403:
    print("(2/4) User Role Test: update:user \n PASSED (403) \n")
else:
    print(f"(2/4) User Role Test: update:user \n FAILED ({test_auth_give_bonus_user_role.status_code}) \n")

test_auth_get_investments_admin_role = get(f"{domain}/user/{foobar}/investments", headers=admin_auth_header)

if test_auth_get_investments_admin_role.status_code == 200:
    print("(3/4) Admin Role Test: read:investments \n PASSED (200) \n")
else:
    print(f"(3/4) Admin Role Test: read:investments \n FAILED ({test_auth_get_investments_admin_role.status_code}) \n")

test_auth_give_bonus_admin_role = patch(f"{domain}/user/{foobar}", json=dict(bonus=float(1)), headers=admin_auth_header)

if test_auth_give_bonus_admin_role.status_code == 202:
    print("(4/4) Admin Role Test: update:user \n PASSED (202) \n")
else:
    print(f"(4/4) Admin Role Test: update:user \n FAILED ({test_auth_give_bonus_admin_role.status_code}) \n")