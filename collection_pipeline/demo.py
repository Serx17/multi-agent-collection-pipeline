import sys
sys.path.append('/content')
from collection_pipeline.models import DebtorRawData
from collection_pipeline.pipeline import CollectionPipeline

def run_demo():
    print("🚀 ЗАПУСК ДЕМО-СИМУЛЯЦИИ")
    print("="*60)

    pipeline = CollectionPipeline()

    # Кейс 1: Успешный
    print("\n1️⃣ КЕЙС: Стандартный должник")
    debtor_1 = DebtorRawData(
        debtor_id="D-001", full_name="Смирнов А.А.", debt_amount=50000,
        days_overdue=45, phone_number="+79991112233"
    )
    res_1 = pipeline.run(debtor_1)
    print(f"   Статус: {res_1['status']}")
    if res_1['status'] == 'completed':
        print(f"   ✅ Скрипт готов. Тон: {res_1['steps'][2].get('name', 'N/A')}")

    # Кейс 2: Должник без телефона (Email/SMS стратегия)
    print("\n2️⃣ КЕЙС: Должник без телефона")
    debtor_2 = DebtorRawData(
        debtor_id="D-002", full_name="Волков Д.Д.", debt_amount=150000,
        days_overdue=120, phone_number=None, email="volkov@test.ru"
    )
    res_2 = pipeline.run(debtor_2)
    print(f"   Статус: {res_2['status']}")
    if res_2['status'] == 'completed':
        print(f"   ✅ Скрипт готов. Канал: {res_2['steps'][1].get('risk', 'N/A')}")

    print("\n✅ ДЕМО ЗАВЕРШЕНО.")

if __name__ == "__main__":
    run_demo()