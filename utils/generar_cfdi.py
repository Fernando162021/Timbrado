from lxml import etree
from datetime import datetime
import os


def generate_cfdi(
        # Datos del emisor
        emisor_rfc="AAA010101AAA",
        emisor_nombre="EMPRESA EMISORA S.A. DE C.V.",
        emisor_regimen_fiscal="601",

        # Datos del receptor
        receptor_rfc="BBB020202BBB",
        receptor_nombre="CLIENTE EJEMPLO",
        receptor_uso_cfdi="G03",

        # Datos del comprobante
        serie="A",
        folio="12345",
        forma_pago="01",  # 01 = Efectivo
        condiciones_pago="Contado",
        lugar_expedicion="64000",  # Código postal
        fecha=None,  # Si es None, se usará la fecha actual

        # Datos del concepto
        concepto_clave="01010101",
        concepto_cantidad=1,
        concepto_unidad="H87",  # H87 = Pieza
        concepto_descripcion="Producto de prueba",
        concepto_valor_unitario=1000.00,

        # Datos de impuestos
        tasa_iva=0.16,

        # Ruta de salida
        output_file="cfdi_ejemplo.xml"
):
    # Asegurarnos que se guarda en la carpeta files/
    # Crear la carpeta si no existe
    os.makedirs("files", exist_ok=True)

    # Añadir el prefijo 'files/' al nombre del archivo
    output_path = os.path.join("files", output_file)

    # Calcular los importes
    concepto_importe = concepto_valor_unitario * concepto_cantidad
    iva_importe = concepto_importe * tasa_iva
    total = concepto_importe + iva_importe

    # Formatear valores numéricos con dos decimales
    concepto_valor_unitario_str = f"{concepto_valor_unitario:.2f}"
    concepto_importe_str = f"{concepto_importe:.2f}"
    iva_importe_str = f"{iva_importe:.2f}"
    subtotal_str = f"{concepto_importe:.2f}"
    total_str = f"{total:.2f}"
    tasa_iva_str = f"{tasa_iva:.6f}"

    # Crear el elemento raíz con sus namespaces
    NSMAP = {
        "cfdi": "http://www.sat.gob.mx/cfd/4",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance"
    }

    # Para atributos con namespace, usamos el método correcto proporcionando el namespace completo
    schema_location_value = "http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"

    comprobante = etree.Element("{http://www.sat.gob.mx/cfd/4}Comprobante", nsmap=NSMAP)
    comprobante.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", schema_location_value)

    # Agregar los atributos al comprobante
    comprobante.set("Version", "4.0")
    comprobante.set("Serie", serie)
    comprobante.set("Folio", folio)
    if fecha:
        comprobante.set("Fecha", fecha)
    else:
        comprobante.set("Fecha", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    comprobante.set("FormaPago", forma_pago)
    comprobante.set("CondicionesDePago", condiciones_pago)
    comprobante.set("SubTotal", subtotal_str)
    comprobante.set("Moneda", "MXN")
    comprobante.set("Total", total_str)
    comprobante.set("TipoDeComprobante", "I")  # I = Ingreso
    comprobante.set("MetodoPago", "PUE")  # PUE = Pago en una sola exhibición
    comprobante.set("LugarExpedicion", lugar_expedicion)

    # Agregar el nodo Emisor
    emisor = etree.SubElement(comprobante, "{http://www.sat.gob.mx/cfd/4}Emisor")
    emisor.set("Rfc", emisor_rfc)
    emisor.set("Nombre", emisor_nombre)
    emisor.set("RegimenFiscal", emisor_regimen_fiscal)

    # Agregar el nodo Receptor
    receptor = etree.SubElement(comprobante, "{http://www.sat.gob.mx/cfd/4}Receptor")
    receptor.set("Rfc", receptor_rfc)
    receptor.set("Nombre", receptor_nombre)
    receptor.set("UsoCFDI", receptor_uso_cfdi)

    # Agregar el nodo Conceptos
    conceptos = etree.SubElement(comprobante, "{http://www.sat.gob.mx/cfd/4}Conceptos")

    # Agregar un concepto
    concepto = etree.SubElement(conceptos, "{http://www.sat.gob.mx/cfd/4}Concepto")
    concepto.set("ClaveProdServ", concepto_clave)
    concepto.set("Cantidad", str(concepto_cantidad))
    concepto.set("ClaveUnidad", concepto_unidad)
    concepto.set("Descripcion", concepto_descripcion)
    concepto.set("ValorUnitario", concepto_valor_unitario_str)
    concepto.set("Importe", concepto_importe_str)

    # Agregar impuestos al concepto
    impuestos_concepto = etree.SubElement(concepto, "{http://www.sat.gob.mx/cfd/4}Impuestos")
    traslados_concepto = etree.SubElement(impuestos_concepto, "{http://www.sat.gob.mx/cfd/4}Traslados")
    traslado_concepto = etree.SubElement(traslados_concepto, "{http://www.sat.gob.mx/cfd/4}Traslado")
    traslado_concepto.set("Base", concepto_importe_str)
    traslado_concepto.set("Impuesto", "002")  # 002 = IVA
    traslado_concepto.set("TipoFactor", "Tasa")
    traslado_concepto.set("TasaOCuota", tasa_iva_str)
    traslado_concepto.set("Importe", iva_importe_str)

    # Agregar el nodo Impuestos (a nivel comprobante)
    impuestos = etree.SubElement(comprobante, "{http://www.sat.gob.mx/cfd/4}Impuestos")
    impuestos.set("TotalImpuestosTrasladados", iva_importe_str)

    traslados = etree.SubElement(impuestos, "{http://www.sat.gob.mx/cfd/4}Traslados")
    traslado = etree.SubElement(traslados, "{http://www.sat.gob.mx/cfd/4}Traslado")
    traslado.set("Base", concepto_importe_str)
    traslado.set("Impuesto", "002")  # 002 = IVA
    traslado.set("TipoFactor", "Tasa")
    traslado.set("TasaOCuota", tasa_iva_str)
    traslado.set("Importe", iva_importe_str)

    # Crear el documento XML
    doc = etree.ElementTree(comprobante)

    # Guardar el XML en un archivo con formato
    with open(output_path, "wb") as f:
        f.write(etree.tostring(
            doc,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        ))

    return output_path