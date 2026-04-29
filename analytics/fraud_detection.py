import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

session_store = {}
ip_store = {}
fraud_alerts = []

class FraudDetector:
    MAX_ORDERS_PER_SESSION = 5
    MAX_AMOUNT_PER_ORDER   = 5000.0
    MAX_DISTINCT_IPS       = 3
    SUSPICIOUS_COUNTRIES   = {"RU", "KP", "IR"}

    def check_order(self, order):
        signals = []
        score   = 0

        if order.get("amount", 0) > self.MAX_AMOUNT_PER_ORDER:
            signals.append("HIGH_AMOUNT")
            score += 30

        session_id = order.get("session_id")
        session    = session_store.get(session_id, {"purchases": 0})
        if session["purchases"] > self.MAX_ORDERS_PER_SESSION:
            signals.append("TOO_MANY_ORDERS_IN_SESSION")
            score += 40
        session["purchases"] += 1
        session_store[session_id] = session

        cid    = order["customer_id"]
        ip_key = f"{cid}_{datetime.now().date()}"
        ips    = ip_store.get(ip_key, set())
        ips.add(order.get("ip_address", "unknown"))
        ip_store[ip_key] = ips
        if len(ips) > self.MAX_DISTINCT_IPS:
            signals.append("MULTIPLE_IPS")
            score += 25

        if order.get("country") in self.SUSPICIOUS_COUNTRIES:
            signals.append("SUSPICIOUS_COUNTRY")
            score += 20

        if order.get("account_age_days", 999) < 7 and order.get("amount", 0) > 500:
            signals.append("NEW_ACCOUNT_HIGH_VALUE")
            score += 35

        if score >= 70:
            risk = "HIGH"
        elif score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        result = {
            "order_id":   order.get("order_id"),
            "risk_score": min(score, 100),
            "risk_level": risk,
            "signals":    signals
        }

        if risk in ("HIGH", "MEDIUM"):
            fraud_alerts.append(result)
            log.warning(f"FRAUD ALERT [{risk}] Order={result['order_id']} Score={result['risk_score']} Signals={signals}")

        return result


detector = FraudDetector()

test_orders = [
    {"order_id": "ORD001", "customer_id": "CUST100", "session_id": "SESS_XYZ",
     "amount": 6500.00, "ip_address": "192.168.1.1", "country": "US", "account_age_days": 365},
    {"order_id": "ORD002", "customer_id": "CUST200", "session_id": "SESS_ABC",
     "amount": 800.00, "ip_address": "10.0.0.5", "country": "RU", "account_age_days": 2},
    {"order_id": "ORD003", "customer_id": "CUST300", "session_id": "SESS_DEF",
     "amount": 120.00, "ip_address": "203.0.113.5", "country": "IN", "account_age_days": 200},
]

for order in test_orders:
    report = detector.check_order(order)
    log.info(f"Order {report['order_id']}: Risk={report['risk_level']} ({report['risk_score']}/100)")

log.info(f"Total fraud alerts: {len(fraud_alerts)}")