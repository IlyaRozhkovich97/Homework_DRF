import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name):
    """Создает продукт в Stripe."""
    try:
        product = stripe.Product.create(name=name)
        return product
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании продукта в Stripe: {e}")


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe."""
    try:
        price = stripe.Price.create(
            unit_amount=amount * 100,
            currency="rub",
            product=product_id,
        )
        return price
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании цены в Stripe: {e}")


def create_stripe_session(price):
    """Создает сессию Stripe."""
    try:
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/",
            line_items=[{"price": price.get("id"), "quantity": 1}],
            mode="payment",
        )
        return session.get("id"), session.get("url")
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка при создании сессии в Stripe: {e}")
