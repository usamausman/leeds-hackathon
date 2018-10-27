package org.name.fingerprintdemo

import android.support.v7.app.AppCompatActivity
import android.os.Bundle

import android.content.Context
import android.app.KeyguardManager
import android.hardware.fingerprint.FingerprintManager

import android.widget.Toast
import android.Manifest
import android.content.pm.PackageManager
import android.support.v4.app.ActivityCompat

import java.security.KeyStore
import android.security.keystore.KeyProperties
import java.security.NoSuchAlgorithmException
import java.security.NoSuchProviderException

import android.security.keystore.KeyGenParameterSpec
import java.security.cert.CertificateException
import java.security.InvalidAlgorithmParameterException
import java.io.IOException

import javax.crypto.KeyGenerator

import android.security.keystore.KeyPermanentlyInvalidatedException
import java.security.InvalidKeyException
import java.security.KeyStoreException
import java.security.UnrecoverableKeyException
import javax.crypto.NoSuchPaddingException
import javax.crypto.SecretKey
import javax.crypto.Cipher

class Fingerprint : AppCompatActivity() {

    private val KEY_NAME = "name_fingerprint_key"

    private var fingerprintManager: FingerprintManager? = null
    private var keyguardManager: KeyguardManager? = null

    private var keyStore: KeyStore? = null
    private var keyGenerator: KeyGenerator? = null

    private var cipher: Cipher? = null

    private var cryptoObject: FingerprintManager.CryptoObject? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_fingerprint)

        if(getManagers()) {
            while(true) {
                generateKey()

                if (cipherInit()) {
                    cipher?.let {
                        cryptoObject = FingerprintManager.CryptoObject(it)
                    }

                    var helper = FingerprintHandler(this)

                    if (fingerprintManager != null && cryptoObject != null) {
                        helper.startAuth(fingerprintManager!!, cryptoObject!!)
                    }
                }
            }
        }
    }

    private fun getManagers(): Boolean {
        fingerprintManager = getSystemService(Context.FINGERPRINT_SERVICE) as FingerprintManager
        keyguardManager = getSystemService(Context.KEYGUARD_SERVICE) as KeyguardManager

        if(keyguardManager?.isKeyguardSecure == false) {
            Toast.makeText(this, "Lock screen security not enabled in Settings", Toast.LENGTH_LONG).show()
            return false
        }

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.USE_FINGERPRINT) !=
            PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(this, "Fingerprint authentication permission not enabled", Toast.LENGTH_LONG).show()

            return false
        }

        if (fingerprintManager?.hasEnrolledFingerprints() == false) {
            Toast.makeText(this, "Register at least one fingerprint in Settings", Toast.LENGTH_LONG).show()
            return false
        }

        Toast.makeText(this, "All good!", Toast.LENGTH_LONG).show()
        return true
    }

    private fun generateKey() {
        try {
            keyStore = KeyStore.getInstance("AndroidKeyStore")
        } catch(e: Exception) {
            e.printStackTrace()
        }

        try {
            keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
        } catch(e: NoSuchAlgorithmException) {
            throw RuntimeException("Failed to get KeyGenerator instance", e)
        } catch(e: NoSuchProviderException) {
            throw RuntimeException("Failed to get KeyGenerator instance", e)
        }

        try {
            keyStore?.load(null)
            keyGenerator?.init(KeyGenParameterSpec.Builder(KEY_NAME,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_CBC)
                .setUserAuthenticationRequired(true)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_PKCS7)
                .build())
            keyGenerator?.generateKey()
        } catch (e: NoSuchAlgorithmException) {
            throw RuntimeException(e)
        } catch (e: InvalidAlgorithmParameterException) {
            throw RuntimeException(e)
        } catch (e: CertificateException) {
            throw RuntimeException(e)
        } catch (e: IOException) {
            throw RuntimeException(e)
        }
    }

    private fun cipherInit(): Boolean {
        try {
cipher = Cipher.getInstance(KeyProperties.KEY_ALGORITHM_AES + "/" +
        KeyProperties.BLOCK_MODE_CBC + "/" +
        KeyProperties.ENCRYPTION_PADDING_PKCS7)
        } catch(e: NoSuchAlgorithmException) {
            throw RuntimeException("Failed to get Cipher", e)
        } catch(e: NoSuchPaddingException) {
            throw RuntimeException("Failed to get Cipher", e)
        }

        try {
            keyStore?.load(null)
            val key = keyStore?.getKey(KEY_NAME, null) as SecretKey
            cipher?.init(Cipher.ENCRYPT_MODE, key)
            return true
        } catch (e: KeyPermanentlyInvalidatedException) {
            return false
        } catch (e: KeyStoreException) {
            throw RuntimeException("Failed to init Cipher", e)
        } catch (e: CertificateException) {
            throw RuntimeException("Failed to init Cipher", e)
        } catch (e: UnrecoverableKeyException) {
            throw RuntimeException("Failed to init Cipher", e)
        } catch (e: IOException) {
            throw RuntimeException("Failed to init Cipher", e)
        } catch (e: NoSuchAlgorithmException) {
            throw RuntimeException("Failed to init Cipher", e)
        } catch (e: InvalidKeyException) {
            throw RuntimeException("Failed to init Cipher", e)
        }
    }
}
