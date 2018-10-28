package org.name.fingerprintdemo

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.fingerprint.FingerprintManager
import android.os.CancellationSignal
import android.support.v4.app.ActivityCompat
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

class FingerprintHandler(private val appContext: Context): FingerprintManager.AuthenticationCallback() {
    private val RPI_IP = "http://10.41.143.40/main.php"

    private var cancellationSignal: CancellationSignal? = null

    fun startAuth(manager: FingerprintManager, cryptoObject: FingerprintManager.CryptoObject) {
        cancellationSignal = CancellationSignal()

        if (ActivityCompat.checkSelfPermission(appContext, Manifest.permission.USE_FINGERPRINT) !=
            PackageManager.PERMISSION_GRANTED) {
            return
        }
        manager.authenticate(cryptoObject, cancellationSignal, 0, this, null)
    }

    override fun onAuthenticationError(errorCode: Int, errString: CharSequence?) {
        Toast.makeText(appContext, "Authentication error\n$errString", Toast.LENGTH_LONG).show()
    }

    override fun onAuthenticationHelp(helpCode: Int, helpString: CharSequence?) {
        Toast.makeText(appContext, "Authentication help\n$helpString", Toast.LENGTH_LONG).show()
        val queue = Volley.newRequestQueue(appContext)
        val stringRequest = object : StringRequest(Request.Method.POST, RPI_IP,
            Response.Listener<String> {},
            Response.ErrorListener {
                Toast.makeText(appContext, "Error", Toast.LENGTH_LONG).show()
            }) {
            override fun getParams(): Map<String, String> {
                val params = HashMap<String, String>()
                params["finger_status"] = "failure"
                return params
            }
        }
        queue.add(stringRequest)
    }

    override fun onAuthenticationFailed() {
        Toast.makeText(appContext, "Authentication failed", Toast.LENGTH_LONG).show()
        val queue = Volley.newRequestQueue(appContext)
        val stringRequest = object : StringRequest(Request.Method.POST, RPI_IP,
            Response.Listener<String> {},
            Response.ErrorListener {
                Toast.makeText(appContext, "Error", Toast.LENGTH_LONG).show()
            }) {
            override fun getParams(): Map<String, String> {
                val params = HashMap<String, String>()
                params["finger_status"] = "failure"
                return params
            }
        }
        queue.add(stringRequest)
    }

    override fun onAuthenticationSucceeded(result: FingerprintManager.AuthenticationResult?) {
        Toast.makeText(appContext, "Authentication succeeded", Toast.LENGTH_LONG).show()
        val queue = Volley.newRequestQueue(appContext)
        val stringRequest = object : StringRequest(Request.Method.POST, RPI_IP,
            Response.Listener<String> {},
            Response.ErrorListener {
                Toast.makeText(appContext, "Error", Toast.LENGTH_LONG).show()
            }) {
            override fun getParams(): Map<String, String> {
                val params = HashMap<String, String>()
                params["finger_status"] = "success"
                return params
            }
        }
        queue.add(stringRequest)
    }
}