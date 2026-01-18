# bot/utils/cart_text.py
def build_cart_text(order) -> str:

# bot/utils/cart_text.py
def build_cart_text(order) -> str:


    lines = ["🧺 <b>Ваша корзина:</b>\n"]





    for item in order.items:


        lines.append(


            f"• {item.product.title} ×{item.qty} — {item.qty * item.product.base_price} ₽"


        )





    lines.append(f"\n💰 <b>Итого:</b> {order.total_price} ₽")


    return "\n".join(lines)





