import javax.net.ssl.*;
import java.io.*;
import java.security.*;
import java.security.cert.Certificate;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

public class Server {

    private static final int delay = 1000;
    private static final String[] protocols = new String[] {"TLSv1.3"};
    private static final String[] cipher_suites = new String[] {"TLS_AES_128_GCM_SHA256"};



    public static void main(String[] args) throws Exception {


        selfSignedCertificate();
        //creating server
        try (BnrServer server = BnrServer.create()) {
            new Thread(server).start();
            Thread.sleep(delay);

            //creating client
            try (SSLSocket socket = createSocket("localhost", server.port())) {
                checkServerCertificate(socket);
                sendHttpRequest(socket);
            }

        }

    }
    private static void selfSignedCertificate() {
        try {
            // Load the keystore.jks with the self-signed certificate
            char[] keystorePassword = System.getProperty("Djavax.net.ssl.keyStorePassword", "passphrase").toCharArray();
            char[] keyPassword = System.getProperty("Djavax.net.ssl.trustStorePassword", "passphrase").toCharArray();

            KeyStore keyStore = KeyStore.getInstance("JKS");
            FileInputStream keyStoreFile = new FileInputStream(System.getProperty("Djavax.net.ssl.keyStore", "keystore.jks"));
            keyStore.load(keyStoreFile, keystorePassword);

            // Initialize the key manager factory
            KeyManagerFactory keyManagerFactory = KeyManagerFactory.getInstance("SunX509");
            keyManagerFactory.init(keyStore, keyPassword);

            // Initialize the SSL context
            SSLContext sslContext = SSLContext.getInstance("TLS");
            sslContext.init(keyManagerFactory.getKeyManagers(), null, null);
        } catch (FileNotFoundException e) {
            System.out.println("Error: Keystore file not found.");
            System.exit(1);
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }

    private static void checkServerCertificate(SSLSocket socket) {
        try {
            SSLSession session = socket.getSession();
            Certificate[] certificates = session.getPeerCertificates();

            if (certificates.length > 0 && certificates[0] instanceof X509Certificate serverCert) {

                // Check if the certificate subject matches the expected value
                if (!serverCert.getSubjectX500Principal().getName().contains("CN=bnr.ro")) {
                    throw new SSLException("Server certificate subject does not match expected value");
                }

                // Check if the certificate issuer matches the expected value
                if (!serverCert.getIssuerX500Principal().getName().contains("CN=bnr.ro")) {
                    throw new SSLException("Server certificate issuer does not match expected value");
                }

                System.out.println("Server certificate is valid.");
            } else {
                throw new SSLException("Invalid server certificate");
            }
        } catch (SSLException e) {
            System.out.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }

    private static void sendHttpRequest(SSLSocket socket) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
             BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            // Send an HTTP GET request
            String request = "GET /bnr HTTP/1.1\r\nHost: bnr.ro\r\nConnection: close\r\n\r\n";
            writer.write(request);
            writer.flush();

            // Read and print the server's response
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        }
    }

    public static SSLSocket createSocket(String host, int port) throws IOException {
        SSLSocket socket = (SSLSocket) SSLSocketFactory.getDefault()
                .createSocket(host, port);
        socket.setEnabledProtocols(protocols);
        socket.setEnabledCipherSuites(cipher_suites);
        return socket;
    }

    public static class BnrServer implements Runnable, AutoCloseable {

        private static final int FREE_PORT = 0;
        private final SSLServerSocket sslServerSocket;

        private BnrServer(SSLServerSocket sslServerSocket) {
            this.sslServerSocket = sslServerSocket;
        }

        public int port() {
            return sslServerSocket.getLocalPort();
        }


        @Override
        public void close() throws Exception {
            if (sslServerSocket != null && !sslServerSocket.isClosed()) {
                sslServerSocket.close();
            }
        }

        @Override
        public void run() {
            System.out.printf("Server started on port %d%n", port());

            try (SSLSocket socket = (SSLSocket) sslServerSocket.accept()) {
                System.out.println("Accepted");
                InputStream is = new BufferedInputStream(socket.getInputStream());
                OutputStream os = new BufferedOutputStream(socket.getOutputStream());
                byte[] data = new byte[2048];
                int len = is.read(data);
                if (len <= 0) {
                    throw new IOException("no data received");
                }
                System.out.printf("Server received %d bytes: %s%n", len, new String(data, 0, len));
                os.write(data, 0, len);
                os.flush();

            } catch (Exception e) {
                System.out.printf("exception: %s%n", e.getMessage());
            }
            System.out.println("Server stopped");
        }

        public static BnrServer create() throws IOException {
            return create(FREE_PORT);
        }

        public static BnrServer create(int port) throws IOException {
            SSLServerSocket socket = (SSLServerSocket) SSLServerSocketFactory.getDefault().createServerSocket(port);
            socket.setEnabledProtocols(protocols);
            socket.setEnabledCipherSuites(cipher_suites);
            return new BnrServer(socket);
        }
    }
}