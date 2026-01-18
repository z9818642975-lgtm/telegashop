# bot/services/salary.py
def calc_operator_salary(

# bot/services/salary.py
def calc_operator_salary(


    *,


    is_meow_kok: bool,


    items_count: int,


) -> int:


    """


    Расчёт зарплаты оператора за смену.





    Правила:


    - если не meow_kok → фикс 750


    - meow_kok:


        ≤ 5 позиций  → 1000


        ≤ 10 позиций → 2000


        далее +1000 за каждые 5 позиций


    """





    if not is_meow_kok:


        return 750





    if items_count <= 5:


        return 1000





    if items_count <= 10:


        return 2000





    extra = items_count - 10


    blocks = (extra + 4) // 5  # округление вверх


    return 2000 + blocks * 1000





