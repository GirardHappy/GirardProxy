import requests,threading,time

class Proxy():
    __country_list = ['all','AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KR', 'KP', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'AN', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW']
    
    def __init__(self,scraper_timeout=60,protocol="socks5",timeout=1000,country=['all'],ssl='all',anonimity="elite",start=True):
        """Create setup and run the Proxy Scraper\n
        ``scraper_timeout`` int
        ``protocol`` ['all','http','socks4','socks5']\n
        ``timeout`` int\n
        ``country`` array containing iso alpha 2 countries or 'all'\n
        ``ssl`` ['all','yes','no']\n
        ``anonimity`` ['elite','anonymous','transparent','all']\n
        ``start`` bool
        """   
        self.setTimeout(scraper_timeout)
        self.setOptions(protocol,timeout,country,ssl,anonimity)
        self.host = ''
        self.port = 0
        self.proxy_data = {}
        self.__threads = []
        if(start):
            self.start()


    def __run(self):
        while(self.__running):
            self.__requestProxy()
            for i in range(self.timeout*10):
                if not self.__running:
                    break
                time.sleep(0.1)
    def __del__(self):
        self.stop()

    def start(self):
        """Start the proxy update loop thread"""
        self.__running = True
        self.__requestProxy()
        self.__caller = threading.Thread(target=self.__run, args=())
        self.__caller.start()

    
    def stop(self):
        """Stop the proxy update loop thread"""
        self.__running = False

    def setTimeout(self,timeout):
        self.timeout = timeout

    def setOptions(self,protocol="socks5",timeout=1000,country=['all'],ssl='all',anonimity="elite"):
        """set the proxy request option\n
        ``protocol`` ['all','http','socks4','socks5']\n
        ``timeout`` int\n
        ``country`` array containing iso alpha 2 countries or 'all'\n
        ``ssl`` ['all','yes','no']\n
        ``anonimity`` ['elite','anonymous','transparent','all']\n
        """    
        Proxy.__checkParams(protocol,timeout,country,ssl,anonimity)
        self.__options = {}
        self.__options['url'] = f"https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol={protocol}&format=json&anonymity={anonimity}&timeout={timeout}&ssl={ssl}&country={','.join(country)}"
        self.__options['protocol'] = protocol
        self.__options['timeout'] = timeout
        self.__options['country'] = country
        self.__options['ssl'] = ssl
        self.__options['anonimity'] = anonimity

    def __checkParams(protocol,timeout,country,ssl,anonimity):
        if not protocol in ['all','http','socks4','socks5']:
            raise Proxy.ProxyError("protocol must be ['all','http','socks4','socks5']")

        if not type(timeout) is int:
            raise Proxy.ProxyError("timout must be an int")

        if not type(country) is list:
            raise Proxy.ProxyError("country must be an array of iso alpha 2 countries or ['all']")

        for c in country:
            if not c in Proxy.__country_list:
                raise Proxy.ProxyError("country must be an iso alpha 2 countries or 'all'")

        if not ssl in ['all','yes','no']:
            raise Proxy.ProxyError("ssl must be ['all','yes','no']")

        if not anonimity in ['elite','anonymous','transparent','all']:
            raise Proxy.ProxyError("anonimity must be ['elite','anonymous','transparent','all']")
    
    def __proxywork(host,port,ip_data):
        try:
            requests.get('https://api.ipify.org', proxies=dict(http=f'socks5://{host}:{port}',https=f'socks5://{host}:{port}'),timeout=0.5)
            return host,port,ip_data,False
        except:
            return None,None,None,True

    def __requestProxy(self):
        r = requests.get(self.__options.get('url')).json()
        for prox in r.get('proxies'):
            t = Proxy.__ReturnValueThread(target=Proxy.__proxywork,args=(prox.get('ip'),prox.get('port'),prox.get('ip_data')))
            t.start()
            self.__threads.append(t)
        while len(self.__threads)>0:
            for t in self.__threads:
                if not t.is_alive():
                    host,port,ip_data,error = t.join()
                    if not error:
                        self.host = host
                        self.port  = int(port)
                        self.proxy_data=ip_data
                        
                    self.__threads.remove(t)
    
    def __str__(self):
        return self.getProxy()

    def getProxy(self):
        """return the proxy addres in the format: ``host:port``"""    
        return f"{self.host}:{self.port}"
    
    class ProxyError(Exception):
        def __init__(self, message):
            self.message = message
    
    class __ReturnValueThread(threading.Thread):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.result = None

        def run(self):
            if self._target is None:
                return
            try:
                self.result = self._target(*self._args, **self._kwargs)
            except Exception as exc:
                Proxy.ProxyError(f'ReturnValueThread Error => {type(exc).__name__}: {exc}')

        def join(self, *args, **kwargs):
            super().join(*args, **kwargs)
            return self.result
