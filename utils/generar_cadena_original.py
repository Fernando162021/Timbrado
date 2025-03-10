from lxml import etree


def generar_cadena_original(xml_path, xslt_path):
    """
    Genera la cadena original de un CFDI a partir de un archivo XML y un archivo XSLT.

    :param xml_path: Ruta al archivo XML del CFDI.
    :param xslt_path: Ruta al archivo XSLT para la transformación.
    :return: La cadena original generada.
    """
    try:
        # Cargar el archivo XML (cfdi_personalizado.xml)
        xml_tree = etree.parse(xml_path)

        # Cargar el archivo XSLT (cadenaoriginal_4_0.xslt)
        xslt_tree = etree.parse(xslt_path)

        # Crear un objeto XSLT
        transform = etree.XSLT(xslt_tree)

        # Realizar la transformación
        resultado = transform(xml_tree)

        # Devolver la cadena original como texto
        return str(resultado).strip()

    except Exception as e:
        print(f"Error generando la cadena original: {e}")
        return None