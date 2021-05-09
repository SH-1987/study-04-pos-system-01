import pandas as pd

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_item_name(self, item_code):
        return self.item_name

    def get_price(self, item_code):
        return self.price        

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.table=pd.DataFrame(index=[], columns=['商品コード','商品名','価格', '個数'])
        self.item_master=item_master
        
    
    def add_item_order(self,item_code, quantity):
        self.order = [item_code, quantity]
        self.item_order_list.append(self.order)

    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{0}".format(item))
    
    def veiw_info(self, item):
        self.table['商品コード']=self.item_order_list
            


### メイン処理
def main():
    # マスタ登録
    item_master=[]
    item_list = pd.read_csv('item_master.csv', dtype={'商品コード':'object', '商品名':'object', '価格':'int'})
    for i in range(len(item_list)):
        item_master.append(Item(item_list["商品コード"].iloc[i],item_list["商品名"].iloc[i],item_list["価格"].iloc[i]))

    # オーダー登録
    df = pd.DataFrame(index=[], columns=['商品コード','商品名','価格', '個数'])
    order=Order(item_master)
    fl = True
    while fl == True:
        oi = input("order codeを入力して下さい>>>")
        q = int(input("個数を入力して下さい>>>"))
        order.add_item_order(oi, q)
        con = input("注文を続けますか？y/n >>>") 
        if con == "y":
            fl = True
        else:
            fl = False


    for o in order.item_order_list:        
        for item in item_master:
            if o[0] == item.item_code:
                a = pd.Series([o[0], item.get_item_name(o[0]), item.get_price(o[0]), o[1]], index=df.columns)
                df = df.append(a, ignore_index=True)

    df['合計価格'] = df['価格'] * df['個数']
    print(df)
    print('合計金額は' + str(sum(df['合計価格']))+'円です')

    payment = int(input("支払い金額を入力してください>>>"))
    if sum(df['合計価格']) > payment:
        print('支払い金額が足りません')
    print('お釣りは'+ str(payment - sum(df['合計価格']))+'円です')

    f = open('recipt.txt', 'w')
    for i in range(len(df)):
        f.write(str(df.iloc[i]))
    f.write("合計金額：" + str(sum(df['合計価格'])) + '\n')
    f.write("お預かり：" + str(payment) + '\n')
    f.write("お釣り:" + str(payment - sum(df['合計価格'])) + '\n')
    f.close()
    # オーダー表示
#    order.view_item_list()
    
if __name__ == "__main__":
    main()