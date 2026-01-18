# bot/services/salary_service.py
def calc_salary(items_count: int, is_meow_kok: bool) -> int:

# bot/services/salary_service.py
def calc_salary(items_count: int, is_meow_kok: bool) -> int:


    """


    Р СџРЎР‚Р В°Р Р†Р С‘Р В»Р В° V1:


    Р’В«Р СљРЎРЏРЎС“ Р С”Р С•Р С”Р’В»


      1РІР‚вЂњ5 РЎв‚¬РЎвЂљ РІвЂ вЂ™ 1000 РІвЂљР…


      6РІР‚вЂњ10 РЎв‚¬РЎвЂљ РІвЂ вЂ™ 2000 РІвЂљР…


      +1000 РІвЂљР… Р В·Р В° Р С”Р В°Р В¶Р Т‘РЎвЂ№Р Вµ РЎРѓР В»Р ВµР Т‘РЎС“РЎР‹РЎвЂ°Р С‘Р Вµ 5 РЎв‚¬РЎвЂљ





    Р С›РЎРѓРЎвЂљР В°Р В»РЎРЉР Р…РЎвЂ№Р Вµ РЎвЂљР С•Р Р†Р В°РЎР‚РЎвЂ№ РІвЂ вЂ™ 750 РІвЂљР… Р В·Р В° Р В·Р В°Р С”Р В°Р В·


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





