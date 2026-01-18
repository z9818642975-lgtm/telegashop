# bot/services/salary_service.py
def calc_salary(items_count: int, is_meow_kok: bool) -> int:

# bot/services/salary_service.py
def calc_salary(items_count: int, is_meow_kok: bool) -> int:


    """


    Правила V1:


    «Мяу кок»


      1–5 шт → 1000 ₽


      6–10 шт → 2000 ₽


      +1000 ₽ за каждые следующие 5 шт





    Остальные товары → 750 ₽ за заказ


    """


    if not is_meow_kok:


        return 750





    if items_count <= 5:


        return 1000


    if items_count <= 10:


        return 2000





    extra = items_count - 10


    blocks = (extra + 4) // 5


    return 2000 + blocks * 1000





