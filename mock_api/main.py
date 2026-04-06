import random
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


def generate_order(i):
    return {
        "order_id": f"ORD{i}",
        "customer_id": f"CUST{random.randint(1, 10)}",
        "amount": round(random.uniform(100, 2000), 2),
        "status": random.choice(["placed", "shipped", "delivered"]),
        "created_at": datetime.utcnow().isoformat(),
    }


@app.get("/orders")
def get_orders(page: int = 1, limit: int = 50):
    start = (page - 1) * limit
    end = start + limit

    data = [generate_order(i) for i in range(start, end)]

    return {"page": page, "total_pages": 2, "data": data}
