package me.fan87.litatomreverse.proxy

import javax.net.ssl.SSLContext
import javax.net.ssl.SSLSocketFactory

class LitProxy(val privateKey: String) {

    val sslContext = SSLContext.getInstance("TLS")

}