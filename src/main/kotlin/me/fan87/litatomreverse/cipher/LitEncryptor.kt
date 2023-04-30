package me.fan87.litatomreverse.cipher

import java.lang.IllegalArgumentException
import java.nio.ByteBuffer
import java.security.SecureRandom
import java.util.*
import javax.crypto.Cipher
import javax.crypto.spec.IvParameterSpec
import javax.crypto.spec.SecretKeySpec

const val COMMON_INITIAL_VECTOR = "abcdef1234567890"

const val SGPOSS_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
const val SECURE_ENDPOINTS_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
const val CHAT_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
const val MODE_1_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
const val MODE_2_KEY = "EIOWUGWOERGJKNLDKGJFOI879KJNSDKJ"
const val MODE_3_KEY = "f1c9208ccd8ef6d85c44b451da593cd4"
const val MODE_4_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
const val MODE_5_KEY = "LTMWUGWOBNLJKIOEKGJFOI256KIOWNKF"


object LitEncryptor {

    fun encryptCustomInitialVector(data: String, key: String, initialVector: ByteArray): String {
        val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.ENCRYPT_MODE, SecretKeySpec(key.encodeToByteArray(), "AES"), IvParameterSpec(initialVector))
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.toByteArray()))
    }
    fun decryptCustomInitialVector(data: String, key: String, initialVector: ByteArray): String {
        val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
        cipher.init(Cipher.DECRYPT_MODE, SecretKeySpec(key.encodeToByteArray(), "AES"), IvParameterSpec(initialVector))
        return cipher.doFinal(
            Base64.getDecoder().decode(data
                .replace("-", "+")
                .replace("_", "/")
                .replace(".", "="))).decodeToString()
    }


    // Key for /lit/lt/sc endpoint
    fun encryptChat(data: String) = encryptBasic(data, CHAT_KEY)
    fun decryptChat(encrypted: String) = decryptBasic(encrypted, CHAT_KEY)
    fun encryptSgposs(data: String) = encryptBasic(data, SGPOSS_KEY)
    fun decryptSgposs(encrypted: String) = decryptBasic(encrypted, SGPOSS_KEY)
    fun encryptSecureEndpoints(data: String) = encryptBasic(data, SECURE_ENDPOINTS_KEY)
    fun decryptSecureEndpoints(encrypted: String) = decryptBasic(encrypted, SECURE_ENDPOINTS_KEY)
    fun decryptBasic(data: String, key: String) = decryptCustomInitialVector(data, key, COMMON_INITIAL_VECTOR.encodeToByteArray())
    fun encryptBasic(data: String, key: String) = encryptCustomInitialVector(data, key, COMMON_INITIAL_VECTOR.encodeToByteArray())


    // LibGuard Base64 encode and decode.
    // LibGuard uses custom Base64 mapping for libguard encryption and decryption. We are guessing that the reason it's using custom is to
    //   1. Strip it a little
    //   2. Extra URL escaping won't be required (As `/` and `+` are escaped in URL)
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



    // Java implementation of LibGuard Protection
    //  - There are 5 modes in LibGuard
    //  - Mode 1, 2, 4, and 5 are basically the same but with different encryption key
    //  - Mode 3 is the most secure one, only used in requests and responses encryption. It takes the current time into account
    // All of those encryption modes are two-way encryption
    fun encryptLibGuard(data: String, mode: Int): String {
        return when (mode) {
            1 -> base64EncodeTransformLibGuard(encryptBasic(data, MODE_1_KEY))
            2 -> base64EncodeTransformLibGuard(encryptBasic(data, MODE_2_KEY))
            3 -> {
                val initialVector = ByteArray(0x10)
                SecureRandom().nextBytes(initialVector)
                val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
                cipher.init(Cipher.ENCRYPT_MODE, SecretKeySpec(MODE_3_KEY.encodeToByteArray(), "AES"), IvParameterSpec(initialVector))
                val encryptedData = cipher.doFinal(data.toByteArray())
                val out = ByteBuffer.allocate(encryptedData.size + 0x10)
                out.put(encryptedData)
                out.put(initialVector)
                out.flip()
                return base64EncodeTransformLibGuard(Base64.getEncoder().encodeToString(out.array()))

            }
            4 -> base64EncodeTransformLibGuard(encryptBasic(data, MODE_4_KEY))
            5 -> base64EncodeTransformLibGuard(encryptBasic(data, MODE_5_KEY))
            else -> throw IllegalArgumentException("Unsupported encryption mode: $mode, valid modes are 1, 2, 3, 4, and 5")
        }
    }

    fun decryptLibGuard(data: String, mode: Int): String {
        return when (mode) {
            1 -> decryptBasic(base64DecodeTransformLibGuard(data), MODE_1_KEY)
            2 -> decryptBasic(base64DecodeTransformLibGuard(data), MODE_2_KEY)
            3 -> {
                val decodedContent = Base64.getDecoder().decode(base64DecodeTransformLibGuard(data)).toList()
                val encryptedContent = decodedContent.let { it.subList(0, it.size - 0x10) }.toByteArray()
                val initialVector = decodedContent.let { it.subList(it.size - 0x10, it.size) }.toByteArray()
                val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
                cipher.init(Cipher.DECRYPT_MODE, SecretKeySpec(MODE_3_KEY.encodeToByteArray(), "AES"), IvParameterSpec(initialVector))
                return cipher.doFinal(encryptedContent).decodeToString()
            }
            4 -> decryptBasic(base64DecodeTransformLibGuard(data), MODE_4_KEY)
            5 -> decryptBasic(base64DecodeTransformLibGuard(data), MODE_5_KEY)
            else -> throw IllegalArgumentException("Unsupported decryption mode: $mode, valid modes are 1, 2, 3, 4, and 5")
        }
    }


}
