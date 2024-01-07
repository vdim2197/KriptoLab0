import javax.net.ssl.SSLPeerUnverifiedException;
import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.net.Socket;
import java.security.cert.Certificate;
import java.security.cert.X509Certificate;

public class TlsClient {

    public static void main(String[] args) {
        String targetHost = "www.bnr.ro";
        int targetPort = 443;

        try {
            SSLSocketFactory socketFactory = (SSLSocketFactory) SSLSocketFactory.getDefault();

            SSLSocket socket = (SSLSocket) socketFactory.createSocket(targetHost, targetPort);

            socket.setEnabledProtocols(socket.getSupportedProtocols());

            socket.setEnabledCipherSuites(socket.getEnabledCipherSuites());

            socket.startHandshake();

            printSslInfo(socket);

            sendHttpRequest(socket);

            saveHtmlContent(socket);

            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void printSslInfo(SSLSocket socket) throws SSLPeerUnverifiedException {
        System.out.println("SSL/TLS Connection Information:");
        System.out.println("Protocol Version:" + socket.getSession().getProtocol());

        Certificate[] certificates = socket.getSession().getPeerCertificates();
        if (certificates.length > 0 && certificates[0] instanceof X509Certificate x509Certificate) {
            System.out.println("Verziószám: " + x509Certificate.getVersion());
            System.out.println("Szériaszám: " + x509Certificate.getSerialNumber());
            System.out.println("Tanúsító hatóság neve: " + x509Certificate.getIssuerX500Principal().getName());
            System.out.println("Kibocsátás dátuma: " + x509Certificate.getNotBefore());
            System.out.println("Érvényességi idő: " + x509Certificate.getNotAfter());
            System.out.println("Tanúsítvány alanya: " + x509Certificate.getSubjectX500Principal().getName());
            System.out.println("Nyilvános kulcs típusa: " + x509Certificate.getPublicKey().getAlgorithm());
            System.out.println("Nyilvános kulcs: " + x509Certificate.getPublicKey());
        }
        System.out.println();

    }

    private static void sendHttpRequest(Socket socket) throws IOException {
        OutputStream outputStream = socket.getOutputStream();
        PrintWriter writer = new PrintWriter(outputStream);

        writer.println("GET /Home.aspx HTTP/1.1");
        writer.println("Host: www.bnr.ro");
        writer.println("Connection: close");
        writer.println();
        writer.flush();
    }

    private static void saveHtmlContent(Socket socket) throws IOException {
        InputStream inputStream = socket.getInputStream();
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr_homepage.txt"))) {
            int bytesRead;
            byte[] buffer = new byte[4096];
            while ((bytesRead = inputStream.read(buffer)) != -1) {
                writer.write(new String(buffer, 0, bytesRead));
            }
        }
    }
}