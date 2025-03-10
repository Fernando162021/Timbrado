from utils.firmar_cfdi import sign_cfdi
from utils.generar_cadena_original import generar_cadena_original
from utils.generar_cfdi import generate_cfdi

"""
custom_xml_file = generate_cfdi(
    # Datos del emisor personalizados
    emisor_rfc="AAA010101AAA",
    emisor_nombre="EMPRESA EMISORA",
    emisor_regimen_fiscal="601",

    # Datos del receptor personalizados
    receptor_rfc="CACX7605101P8",
    receptor_nombre="XOCHILT CASAS CHAVEZ",
    receptor_uso_cfdi="G03",

    # Personalizar otros campos
    serie="A",
    folio="12345",
    lugar_expedicion="36257",  # Código postal del receptor

    # Datos del producto
    concepto_descripcion="Producto de prueba",
    concepto_valor_unitario=1000.00,
    concepto_cantidad=1,

    # Archivo de salida personalizado
    output_file="cfdi_personalizado.xml"
)
print(f"CFDI personalizado generado exitosamente en el archivo: {custom_xml_file}")
"""

xml_file = 'files/cfdi_personalizado.xml'  # Ruta al archivo XML
xslt_file = 'files/cadenaoriginal_4_0.xslt'  # Ruta al archivo XSLT

# Ruta al archivo de clave privada .key y certificado .cer
key_path = 'files/Claveprivada_FIEL_CACX7605101P8_20230509_114423.key'  # Actualiza la ruta
cert_path = 'files/cacx7605101p8.cer'  # Actualiza la ruta
password = "12345678a"

cadena_original = generar_cadena_original(xml_file, xslt_file)

sello_digital = sign_cfdi(cadena_original, key_path, password)

# Mostrar el sello generado
print("Sello digital:", sello_digital)