from utils.convert_der_to_pem import convert_der_to_pem
from utils.firmar_cfdi import sign_cfdi, incrustar_sello_en_xml
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
key_path = 'files/Claveprivada_FIEL_CACX7605101P8.pem'  # Actualiza la ruta
cert_path = 'files/cacx7605101p8.cer'  # Actualiza la ruta
password = '12345678a'

cadena_original = generar_cadena_original(xml_file, xslt_file)

sello_digital = sign_cfdi(cadena_original, key_path, password)

# Llamar a la función para incrustar el sello en el XML
xml_con_sello = incrustar_sello_en_xml(xml_file, sello_digital)

# Mostrar el archivo con el sello incrustado
print(f"Archivo XML con el sello incrustado: {xml_con_sello}")

# Timbrar el CFDI con el PAC
resultado_timbrado = timbrar_cfdi(xml_con_sello)
if resultado_timbrado.get("success", False):
    print(f"CFDI timbrado exitosamente!")
    print(f"Archivo timbrado guardado en: {resultado_timbrado.get('archivo_timbrado')}")
else:
    print(f"Error al timbrar: {resultado_timbrado.get('error')}")

"""
# Ruta de archivos
der_key_path = "files/Claveprivada_FIEL_CACX7605101P8_20230509_114423.key"
pem_key_path = "files/Claveprivada_FIEL_CACX7605101P8.pem"

# Convertir clave
convert_der_to_pem(der_key_path, pem_key_path, "12345678a")

print(f"Clave convertida y cifrada: {pem_key_path}")
"""

