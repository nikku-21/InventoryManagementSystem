"""Unit tests for validation, stock rules, login and FMEA maths (Poka-Yoke checks)."""
import os
import tempfile

os.environ["INVENTORY_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")   # before app imports

import pytest  # noqa: E402

from app import auth, services  # noqa: E402
from app.db import Base, engine  # noqa: E402
from app.models import FmeaItem, Product  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    auth.session.close()
    Base.metadata.drop_all(engine)
    services.init_db()
    yield


def make_product(**kw):
    data = {"sku": "ab-1", "name": "Pen", "quantity": 5, "reorder_level": 2, "unit_price": 1.5}
    data.update(kw)
    return services.save(Product, data)


def test_login_success_and_failure():
    assert auth.authenticate("admin", "Admin@123").role == "admin"
    assert auth.authenticate("admin", "wrong") is None


def test_password_is_hashed():
    user = auth.authenticate("admin", "Admin@123")
    assert user.password_hash != "Admin@123" and user.password_hash.startswith("$2")


def test_sku_is_uppercased_and_unique():
    assert make_product().sku == "AB-1"
    with pytest.raises(ValueError):
        make_product()


def test_negative_values_rejected():
    with pytest.raises(ValueError):
        make_product(sku="X1", quantity=-1)


def test_required_name():
    with pytest.raises(ValueError):
        make_product(sku="X2", name="  ")


def test_stock_in_and_out():
    p = make_product()
    services.stock_move(p.id, "IN", 10)
    assert services.stock_move(p.id, "OUT", 3).quantity == 12


def test_cannot_issue_more_than_stock():
    p = make_product()
    with pytest.raises(ValueError):
        services.stock_move(p.id, "OUT", 99)


def test_low_stock_list():
    make_product(quantity=1)
    assert len(services.low_stock()) == 1


def test_fmea_rpn_and_range():
    row = services.save(FmeaItem, {"failure_mode": "x", "severity": 5, "occurrence": 4, "detection": 3})
    assert row.rpn == 60
    with pytest.raises(ValueError):
        services.save(FmeaItem, {"failure_mode": "y", "severity": 11})
