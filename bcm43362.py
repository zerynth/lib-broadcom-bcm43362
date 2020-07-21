"""
.. module:: bcm43362

***************
BCM43362 Module
***************



This module implements the bcm43362 wifi driver. At the moment some functionalities are missing:

    * soft ap
    * wifi direct


It can be used for every kind of bcm43362 based device, going from the Particle Photon to
Broadcom Evaluation Boards (not integrated in the IDE).

It is important to remark that Broadcom drivers for Zerynth are distributed as binary only, since the Broadcom license for
source code is very restrictive.

The bcm43362 is based on the SDIO standard and also needs some additional pins to function; one which is called WEN (Wireless Enable) used as turn on/shutdown;
one which is called RST and is used internally to reset the Wifi chip; more info on Broadcom Community: https://community.broadcom.com


To use the module expand on the following example: ::

    from broadcom.bcm43362 import bcm43362 as bcm
    from wireless import wifi

    bcm.auto_init()
    for retry in range(10):
        try:
            wifi.link("Network-SSID", wifi.WIFI_WPA2, "password")
            break
        except Exception as e:
            print(e)

    if not wifi.is_linked():
        raise IOError

    """



#-if BCM43362__RVO
### RVO
@native_c("bcm_init",
    [
    "#csrc/misc/zstdlib.c",
    ##-if ZERYNTH_SSL
    "#csrc/tls/mbedtls/library/*",
    ##-endif
    "#csrc/zsockets/*",
    "#csrc/hwcrypto/*",
    ],
    ["VHAL_SDIO"],
    [
    ##-if ZERYNTH_SSL
    "-I#csrc/tls/mbedtls/include",
    ##-endif
    "-I#csrc/zsockets",
    "-I#csrc/hwcrypto",
    "-I.../src/lwip",
    "-I.../src/lwip/include",
    "-I.../src/lwip/include/ipv4",
    ])
def _hwinit(boots0,boots1,wen,rst,country):
    pass
#-else
### SDIO from source
@native_c("bcm_init",
    ["csrc/ifc/wwd_ifc.c",
    "csrc/ifc/bcm_host_rtos.c",
    "csrc/ifc/bcm_host_platform.c",
    "csrc/ifc/bcm_host_bus_sdio.c",
    "src/lwip/arch/*",
    ##-if ZERYNTH_SSL
    "#csrc/tls/mbedtls/library/*",
    ##-endif
    ##-if !BCM43362_BUILD_RVO
    "#csrc/misc/zstdlib.c",
    "#csrc/zsockets/*",
    "#csrc/hwcrypto/*",
    ##-endif
    "csrc/WWD/internal/*",
    "csrc/WWD/internal/bus_protocols/*",
    "csrc/WWD/internal/bus_protocols/SDIO/*",
    "csrc/resources/*",
    "csrc/platform/*",
    "csrc/libraries/utilities/TLV/*",
    "csrc/network/LwIP/WWD/*",
    "csrc/WWD/internal/chips/43362A2/*",
    "csrc/network/LwIP/ver/src/api/api_lib.c",
    "csrc/network/LwIP/ver/src/api/api_msg.c",
    "csrc/network/LwIP/ver/src/api/err.c",
    "csrc/network/LwIP/ver/src/api/netbuf.c",
    "csrc/network/LwIP/ver/src/api/netdb.c",
    "csrc/network/LwIP/ver/src/api/netifapi.c",
    "csrc/network/LwIP/ver/src/api/sockets.c",
    "csrc/network/LwIP/ver/src/api/tcpip.c",
    "csrc/network/LwIP/ver/src/core/dhcp.c",
    "csrc/network/LwIP/ver/src/core/dns.c",
    "csrc/network/LwIP/ver/src/core/init.c",
    "csrc/network/LwIP/ver/src/core/ipv4/autoip.c",
    "csrc/network/LwIP/ver/src/core/ipv4/icmp.c",
    "csrc/network/LwIP/ver/src/core/ipv4/igmp.c",
    "csrc/network/LwIP/ver/src/core/ipv4/inet.c",
    "csrc/network/LwIP/ver/src/core/ipv4/inet_chksum.c",
    "csrc/network/LwIP/ver/src/core/ipv4/ip.c",
    "csrc/network/LwIP/ver/src/core/ipv4/ip_addr.c",
    "csrc/network/LwIP/ver/src/core/ipv4/ip_frag.c",
    "csrc/network/LwIP/ver/src/core/def.c",
    "csrc/network/LwIP/ver/src/core/timers.c",
    "csrc/network/LwIP/ver/src/core/mem.c",
    "csrc/network/LwIP/ver/src/core/memp.c",
    "csrc/network/LwIP/ver/src/core/netif.c",
    "csrc/network/LwIP/ver/src/core/pbuf.c",
    "csrc/network/LwIP/ver/src/core/raw.c",
    "csrc/network/LwIP/ver/src/core/snmp/asn1_dec.c",
    "csrc/network/LwIP/ver/src/core/snmp/asn1_enc.c",
    "csrc/network/LwIP/ver/src/core/snmp/mib2.c",
    "csrc/network/LwIP/ver/src/core/snmp/mib_structs.c",
    "csrc/network/LwIP/ver/src/core/snmp/msg_in.c",
    "csrc/network/LwIP/ver/src/core/snmp/msg_out.c",
    "csrc/network/LwIP/ver/src/core/stats.c",
    "csrc/network/LwIP/ver/src/core/sys.c",
    "csrc/network/LwIP/ver/src/core/tcp.c",
    "csrc/network/LwIP/ver/src/core/tcp_in.c",
    "csrc/network/LwIP/ver/src/core/tcp_out.c",
    "csrc/network/LwIP/ver/src/core/udp.c",
    "csrc/network/LwIP/ver/src/netif/etharp.c",
    ],
    ["VHAL_SDIO",
    'WICED_VERSION=\"3.3.1\"',
    'BUS=\\\"SDIO\\\"',
    'BUS_IS_SDIO',
    'PLATFORM=\\\"BCM943362WCD4\\\"',
    ],
    [
    "-I.../csrc/include",
    "-I.../csrc/ifc",
    "-I.../src/lwip",
    "-I.../csrc/WWD/include",
    "-I.../csrc/network/NoNS/WWD",
    "-I.../csrc/WWD/internal/bus_protocols/SDIO",
    "-I.../csrc/WWD",
    "-I.../csrc/WWD/internal/chips/43362A2",
    "-I.../csrc/libraries/utilities/TLV",
    "-I.../csrc/WWD/include/network",
    "-I.../csrc",
    "-I.../csrc/BCM943362WCD4",
    "-I.../csrc/network/LwIP/WWD",
    "-I.../src/lwip/include",
    "-I.../src/lwip/include/ipv4",
    ##-if ZERYNTH_SSL
    "-I#csrc/tls/mbedtls/include",
    ##-endif
    "-I#csrc/zsockets",
    "-IU#csrc/hwcrypto",
    ])
def _hwinit(boots0,boots1,wen,rst,country):
    pass
#-endif

def auto_init(country="US"):
    """
.. function:: auto_init(country="US")

        Tries to automatically init the bcm43362 driver by looking at the device type.
        The automatic configuration is possible for Broadcom Evaluation devices and Particle Photon (both USI9 and USI14 modules).

        The *country* argument initializes the driver to use only country available channels.

        PeripheralError is raised in case of failed initialization.
    """
    if __defined(BOARD,"bcm943362wcd4"):
        init(D11,D12,D13,D14,country)
    elif __defined(BOARD,"particle_photon"):
        init(D16,D17,D18,D19,country)
    elif __defined(BOARD,"sparkfun_photon"):
        init(0xffff,0xffff,D20,D19,country)
    elif __defined(CDEFS,"BCM_BOARD_EMW3166"):
        init(0xffff,0xffff,0xffff,D27,country)
    else:
        raise UnsupportedError

def init(boots0,boots1,wen,rst,country):
    """
.. function:: init(boots0,boots1,wen,rst,country)

        Tries to init the bcm43362 driver:

            * *boots0* and *boots1* are the pins used to configure the chip transfer (SPI vs SDIO). Pass 0xffff if not needed.
            * *wen* is the pin used as wifi power switch
            * *rst* is the pin used as wifi reset
            * *country* is the two letter code of the country. It is used to identify available channels.

    """
    _hwinit(boots0,boots1,wen,rst,country)
    __builtins__.__default_net["wifi"] = __module__
    __builtins__.__default_net["sock"][0] = __module__ #AF_INET
    __builtins__.__default_net["ssl"] = __module__

#-if BCM43362__RVO
#ugly hack to select correct firmware
if __defined(CDEFS,"BCM_BOARD_WM_N_BM_09"):
    __cfile("rvo/bcm43362_usi9.rvo")
elif __defined(CDEFS,"BCM_BOARD_WM_N_BM_14"):
    __cfile("rvo/bcm43362_usi14.rvo")
elif __defined(CDEFS,"BCM_BOARD_EMW3166"):
    __cfile("rvo/bcm43362_emw3166.rvo")
#-endif


@native_c("bcm_wifi_link",[],[])
def link(ssid,sec,password):
    pass

@native_c("bcm_wifi_is_linked",[],[])
def is_linked():
    pass


@native_c("bcm_scan",["csrc/*"])
def scan(duration):
    pass

@native_c("bcm_wifi_unlink",["csrc/*"])
def unlink():
    pass


@native_c("bcm_link_info",["csrc/*"])
def link_info():
    pass

@native_c("bcm_set_link_info",["csrc/*"])
def set_link_info(ip,mask,gw,dns):
    pass

@native_c("bcm_resolve",["csrc/*"])
def gethostbyname(hostname):
    pass


@native_c("py_net_socket",["csrc/*"])
def socket(family,type,proto):
    pass

@native_c("py_net_setsockopt",["csrc/*"])
def setsockopt(sock,level,optname,value):
    pass


@native_c("py_net_close",["csrc/*"])
def close(sock):
    pass


@native_c("py_net_sendto",["csrc/*"])
def sendto(sock,buf,addr,flags=0):
    pass

@native_c("py_net_send",["csrc/*"])
def send(sock,buf,flags=0):
    pass

@native_c("py_net_send_all",["csrc/*"])
def sendall(sock,buf,flags=0):
    pass


@native_c("py_net_recv_into",["csrc/*"])
def recv_into(sock,buf,bufsize,flags=0,ofs=0):
    pass


@native_c("py_net_recvfrom_into",["csrc/*"])
def recvfrom_into(sock,buf,bufsize,flags=0):
    pass


@native_c("py_net_bind",["csrc/*"])
def bind(sock,addr):
    pass

@native_c("py_net_listen",["csrc/*"])
def listen(sock,maxlog=2):
    pass

@native_c("py_net_accept",["csrc/*"])
def accept(sock):
    pass

@native_c("py_net_connect",["csrc/*"])
def connect(sock,addr):
    pass

@native_c("py_net_select",[])
def select(rlist,wist,xlist,timeout):
    pass

@native_c("py_secure_socket",[],[])
def secure_socket(family, type, proto, ctx):
    pass

@native_c("bcm_set_antenna",[])
def set_antenna(antenna):
    """
.. function:: set_antenna(antenna)

    Selects the antenna to be used:

        * 0: antenna 0
        * 1: antenna 1
        * 3: automatic antenna selection

    """
    pass

@native_c("bcm_rssi",[])
def get_rssi():
    """
.. function:: get_rssi()

    Returns the current RSSI in dBm

    """
    pass

@native_c("bcm_last_error",[])
def get_error():
    """
.. function:: get_error()

    Returns the last connection error as an internal code.

    """
    pass


