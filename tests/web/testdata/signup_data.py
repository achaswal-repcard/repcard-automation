import time

import pytest


@pytest.fixture
def realistic_signup_data():
    ts = int(time.time())
    return {
        "first_name": "Olivia",
        "last_name": "Bennett",
        "email": f"olivia.bennett{ts}@mailinator.com",
        "password": "SecurePass@123",
        "username": f"oliviab{ts}",
        "phone": "4155550126",
        "company_name": "Northwind Advisory Group",
        "industry": "Agency",
        "job_title": "Client Success Manager",
        "website": "https://northwindadvisory.com",
        "bio": (
            "I help local businesses improve customer communication, "
            "lead follow-up, and online reputation through consistent workflows."
        ),
        "opt_in_marketing": True,
    }
