from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from lxml import etree
from pycfdi import Cfdi
import base64


def sign_cfdi(cadena_original, key_path, password):
    """
    Firma la cadena original del CFDI con la llave privada del CSD.

    :param cadena_original: La cadena original generada del CFDI.
    :param key_path: Ruta del archivo .key (llave privada).
    :param password: Contraseña del archivo .key.
    :return: Sello digital en formato base64.
    """
    # Leer la llave privada (.key) y decodificarla con la contraseña
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password.encode() if password else None,  # Convertir la contraseña a bytes
            backend=default_backend()
        )

    # Firmar la cadena original con SHA-256 y RSA
    signature = private_key.sign(
        cadena_original.encode(),  # Convertir la cadena a bytes
        padding.PKCS1v15(),  # Padding estándar para CFDI
        hashes.SHA256()
    )

    # Convertir la firma a Base64
    sello = base64.b64encode(signature).decode("utf-8")
    return sello


def incrustar_sello_en_xml(xml_file, sello_digital):
    # Leer el archivo XML
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Incrustar el sello digital en el nodo 'Comprobante'
    root.set("Sello", sello_digital)

    # Guardar el XML con el sello incrustado
    xml_con_sello = xml_file.replace(".xml", "_con_sello.xml")
    tree.write(xml_con_sello, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    return xml_con_sello