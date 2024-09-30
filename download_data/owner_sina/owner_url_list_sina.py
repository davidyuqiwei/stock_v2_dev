
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
    
    def owner_merrill_lynch(self):
        """
        MERRILL LYNCH
        """
        return "sina_owner_merrill_lynch","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=300711&stockholderid=80051610"

    def owner_maucau_finance(self):
        """
        澳门金融管理局
        """
        return "sina_owner_maucau_finance","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=600008&stockholderid=70304274"
    
    def owner_gaosheng(self):
        """
        高盛公司有限责任公司
        """
        return "sina_owner_gaosheng","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=605303&stockholderid=81568202"
    
    def owner_keweite(self):
        """
        科威特投资局
        """
        return "sina_owner_keweite","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=002154&stockholderid=80195934"

    def owner_UBSAG(self):
        return "sina_owner_UBSAG","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=300012&stockholderid=80044863"
    
    def owner_CITIGROUP(self):
        return "sina_owner_CITIGROUP","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=300041&stockholderid=80044819"

    def owner_JPMorgan(self):
        return "sina_owner_JPMorgan","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=300269&stockholderid=70306761"

    def owner_MORGAN_STANLEY(self):
        return "sina_owner_MORGAN_STANLEY","https://vip.stock.finance.sina.com.cn/corp/view/vCI_HoldStockState.php?stockid=300269&stockholderid=80044862"
    def sina_owner_list(self):
        owner_list = [
            self.owner_abdb(),
            self.owner_shebao102(),
            self.owner_shebao406(),
            self.owner_hkjiesuan(),
            self.owner_merrill_lynch(),
            self.owner_maucau_finance(),
            self.owner_keweite(),
            self.owner_UBSAG(),
            self.owner_CITIGROUP(),
            self.owner_JPMorgan(),
            self.owner_MORGAN_STANLEY()
        ]
        return owner_list
    
if __name__ == '__main__':
    aa = DataURLSina().sina_owner_list()
    print(aa)
