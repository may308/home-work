import json

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_data(filename: str) -> list:
    """載入 JSON 檔案內容，若檔案不存在或為空則回傳空列表"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(filename: str, orders: list) -> None:
    """將訂單資料寫入指定 JSON 檔案"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)


def calculate_order_total(order: dict) -> int:
    """計算單筆訂單的總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])


def print_order_report(data: list, title="訂單報表", single=False) -> None:
    """列印訂單報表"""
    print(
        f"\n{'=' * 20} {title} {'=' * 20}"
    )
    if not single:
        for idx, order in enumerate(data, 1):
            print(f"訂單 #{idx}")
            _print_single_order(order)
    else:
        _print_single_order(data)
    print("=" * 50)


def _print_single_order(order: dict) -> None:
    """列印單一訂單詳細內容"""
    print(f"訂單編號: {order['order_id']}")
    print(f"客戶姓名: {order['customer']}")
    print("-" * 50)
    print("商品名稱\t單價\t數量\t小計")
    print("-" * 50)
    total = 0
    for item in order["items"]:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        print(
            f"{item['name']}\t{item['price']}\t"
            f"{item['quantity']}\t{subtotal}"
        )
    print("-" * 50)
    print(f"訂單總額: {total}")
    print("=" * 50)


def add_order(orders: list) -> str:
    """新增訂單"""
    order_id = input("請輸入訂單編號：").strip().upper()
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：").strip()
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if not name:
            break
        while True:
            try:
                price = input("請輸入價格：").strip()
                price = int(price)
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        while True:
            try:
                quantity = input("請輸入數量：").strip()
                quantity = int(quantity)
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    new_order = {"order_id": order_id, "customer": customer, "items": items}
    orders.append(new_order)
    save_orders(INPUT_FILE, orders)
    return f"=> 訂單 {order_id} 已新增！"


def process_order(orders: list) -> tuple:
    """處理出餐訂單，從 orders.json 搬移到 output_orders.json"""
    if not orders:
        return "=> 無待處理訂單", None

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, 1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
        if not choice:
            return "=> 已取消出餐處理", None
        if (
            not choice.isdigit()
            or int(choice) < 1
            or int(choice) > len(orders)
        ):
            print("=> 錯誤：請輸入有效的數字")
            continue

        index = int(choice) - 1
        order = orders.pop(index)

        completed_orders = load_data(OUTPUT_FILE)
        completed_orders.append(order)

        save_orders(INPUT_FILE, orders)
        save_orders(OUTPUT_FILE, completed_orders)

        return f"=> 訂單 {order['order_id']} 已出餐完成", order


def main() -> None:
    """主程式流程"""
    while True:
        print("\n***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()
        orders = load_data(INPUT_FILE)

        if not choice:
            break
        elif choice == "1":
            result = add_order(orders)
            print(result)
        elif choice == "2":
            print_order_report(orders)
        elif choice == "3":
            result, processed_order = process_order(orders)
            print(result)
            if processed_order:
                print("\n出餐訂單詳細資料：")
                print_order_report(processed_order, title="出餐訂單", single=True)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")


if __name__ == "__main__":
    main()
