class DataURLSina:
    def __init__(self):
        self.test = ""

    def owner_abdb(self):
        """
        阿布达比
        :return:
        """
        return "sina_owner_abudabi","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=000887&stockholderid=80128964"

    def owner_shebao102(self):
        """
        社保
        :return:
        """
        return "sina_owner_shebao102","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=000887&stockholderid=70010102"
    
    def owner_shebao406(self):
        return "sina_owner_shebao406","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=600867&stockholderid=70010406"
    
    def owner_hkjiesuan(self):
        """
        香港中央结算有限公司
        :return:
        """
        return "sina_owner_hkjiesuan","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=601398&stockholderid=80568462"
    
    def sina_owner_list(self):
        owner_list = [
            self.owner_abdb(),
            self.owner_shebao102(),
            self.owner_shebao406(),
            self.owner_hkjiesuan(),
        ]
        return owner_list