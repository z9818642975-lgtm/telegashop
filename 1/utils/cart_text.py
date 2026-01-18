# bot/utils/cart_text.py
def build_cart_text(order) -> str:

# bot/utils/cart_text.py
def build_cart_text(order) -> str:


    lines = ["СЂСџВ§С” <b>Р вЂ™Р В°РЎв‚¬Р В° Р С”Р С•РЎР‚Р В·Р С‘Р Р…Р В°:</b>\n"]





    for item in order.items:


        lines.append(


            f"РІР‚Сћ {item.product.title} Р“вЂ”{item.qty} РІР‚вЂќ {item.qty * item.product.base_price} РІвЂљР…"


        )





    lines.append(f"\nСЂСџвЂ™В° <b>Р ВРЎвЂљР С•Р С–Р С•:</b> {order.total_price} РІвЂљР…")


    return "\n".join(lines)





