# Litatom Reverse Engineer Project

**Author:** fan87 / TropicalFan344

*NOT affiliated or associated with Construct Technology PTE. LTD.*


## I. Introduction
Litatom (Also known as Litmatch) is a networking/social Android app built with Java and
Kotlin. It's a full stack app as it has a fully functional backend (Instead of a simple firebase
database). It has some security features, and we thought it's worth doing research
on Litatom.

The app package name is `com.litatom.app`, in the time of researching, the latest
version is `6.15.0`, the API may differ in future updates.

The app doesn't support x86 devices, you may have to install 
`libhoudini` or use an actual ARM device for this.


### Reversing Environment Setup
> ⚠ This section is only for people who want to reverse the app

It's recommended to use an actual ARM device as Gdb could not debug libraries
loaded with `libhoudini`, although it's not needed, but still recommended.

It's also recommended to have root on the device, you can easily debug apps
without any difficulties.

Our setup is Raspberry Pi 4 with [KonstaKANG's LineageOS Build](https://konstakang.com/devices/rpi4/AOSP13/)
with Gapps and Magisk (Means we have root access). We were originally using `Waydroid`, it will work if you are only gonna
be hooking into Java functions using `Frida` or MITM (Man-in-the-middle) HTTP requests.


## II. Requests/Responses
Litatom app starts an OkHttp instance with SSL Pinning (Optional) on start with base
URL of `www.litatom.com` (In `6.15.0`). The SSL pinning is optional because
it could be disabled by changing `remote_config` configuration in Google Play Measurement.

To bypass SSL pinning, you either modify `remote_config` from Google Play Service Measurement (Requires root),
or use `frida` or other tools to hook into the LitNetwork initialization method
(Where it initializes the OkHttp client), and modify the remote config before, which is 
the method we have chosen to use.

The frida script is quiet simple, it does literal what it is.

Note that the mapping may differ on your side, but you find where it initializes
OkHttp Client anyway.

```ts
const LitNetwork = Java.use("b.f0.a.d"); // com.lit.net.LitNetwork
LitNetwork.b.implementation = function( // Init function
    context: any,
    config: any
) {
    console.log("Pre initialize   " + config.g.value)
    config.g.value = false; // config.enable_ssl_pin = true
    this.b(context, config); // this.init(context, config);
    console.log("Post initialize  " + config.g.value)
}
```

## III. Logging
The logging is using [Tencent's Mars Logging Library](https://github.com/Tencent/mars/tree/master/mars/log) and
encrypted using a public key. The log will be uploaded to Litatom.

To enable logging (For reversing), you can hook into the library itself using Frida, it will also print out if the SSL Unpinning is successfully or not.

## IV. Encryption
Request bodies and some of the response bodies (That has `application/x-litatom-json` as content type)
are encrypted using `LibGuard`. There are also pure-java encryption method
included in the APK, it's used to encrypt Chat messages, encrypt basic parameters
(For SMS Login, Google Login, FaceBook Login, or Get User Info endpoints, and 
a weird one (check if it's contains `sgposs` in host?)).

The keys could be extracted from `com.lit.app.net.interceptors(?).BasicParamsInterceptor`
(Name is deobfuscated with the proguard rules applied and debug annotations kept in
compiled Kotlin bytecode). This 
includes the key that's used to encrypt chat messages as it's duplicated, but
if it's changed it could be extracted from `com.lit.app.im.IMModel` class (Obfuscated)


Here's the extracted keys for the current version
```js
SGPOSS_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
SECURE_ENDPOINTS_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
CHAT_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
MODE_1_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
MODE_2_KEY = "EIOWUGWOERGJKNLDKGJFOI879KJNSDKJ"
MODE_3_KEY = "f1c9208ccd8ef6d85c44b451da593cd4"
MODE_4_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
MODE_5_KEY = "LTMWUGWOBNLJKIOEKGJFOI256KIOWNKF"
```

As mentioend above, Libguard mode 3 is a little more secure, it uses random with `time()` as seed, 
and generate 16 bytes of IV parameter. Then it appends the generated IV to the encrypted token, than Base64 it. LibGuard also uses a different Base64 mapping:
```kt
fun base64DecodeTransformLibGuard(data: String): String {
    return data.replace("-", "+")
        .replace("_", "/")
        .replace(".", "=")
}
fun base64EncodeTransformLibGuard(data: String): String {
    return data.replace("+", "-")
        .replace("/", "_")
        .replace("=", ".")
}
```

We suspect it's there because it doesn't need to escape `/` and `+` for url, and also strip it a little so it's harder to figure out what it's about.

## Conclusion, what we've learned
We've found a few problems with Litmatch. First, obviously is the request and response
encryption. It's using AES, which is not really secure for man-in-the-middle attack,
there's basically no reason of using AES from security standpoint. A RSA encryption
could improve things, so it will be much more difficult to reverse Http requests by
simply decrypting them - because we don't have the private key.

It's also using a fixed Initial Vector Parameter for AES in both LibGuard encryption
mode 1, 2, 4, 5, and pure-java encryption (It's supposed to be random. but in the code
it's always `abcdef1234567890`), while mode 3 is the s standard way of AES CBC encryption.

From a Minecraft premium client developer standpoint, the obfuscation is too weak, we
do know that most Android apps don't need obfuscation, but Proguard isn't even stripping
the source file name, which I find it really weird, With source file name stripped,
it would be much much harder to reverse.

It seems like everything is in conflict to us, it got RSA for logging encryption
, but then it uses AES with fixed IV to encrypt and decrypt requests and responses;
It got `libguard` as native library, while it could be easily implemented with Java or
Kotlin, which sounds like they want to prevent reversers, but they didn't even
bother to remove function names from the native library, or even remove source file name
from compiled Kotlin classes.

I have no mean to say that Construct Tech is bad, because compare to 90% of the apps on
the market, it's secure enough, but there are definitely room for improvement.

<br>
<br>

<p align="center">(c) fan87, TropicalFan344  All rights reserves</p>

