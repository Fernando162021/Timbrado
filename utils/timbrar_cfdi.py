from typing import Any, Optional
from requests import Response, request
import json
from pathlib import Path

def timbrar_cfdi(xml_path: str) -> dict:
    """
    Timbra un CFDI usando el servicio de SW (ambiente de pruebas)
    
    Args:
        xml_path: Ruta al archivo XML del CFDI sellado
        
    Returns:
        dict: Respuesta del servicio de timbrado
    """
    # URL del servicio de autenticación
    url_auth: str = "https://services.test.sw.com.mx/v2/security/authenticate"

    # Credenciales de prueba
    payload: str = json.dumps({
        "user": " usuario@pruebas.com",
        "password": "contraseña1234"
    })
    
    headers: dict = {"Content-Type": "application/json"}

    # Obtener token de autenticación
    try:
        response: Response = request("POST", url_auth, headers=headers, data=payload)
        response.raise_for_status()
        
        auth_data: dict = response.json()
        if not auth_data.get("data", {}).get("token"):
            raise ValueError("No se obtuvo token de autenticación")
            
        token: str = auth_data["data"]["token"]
    except Exception as e:
        return {"success": False, "error": f"Error de autenticación: {str(e)}"}

    # URL del servicio de timbrado
    url_stamp: str = "https://services.test.sw.com.mx/v4/cfdi33/stamp/v4"

    # Preparar archivo XML para envío
    try:
        with open(xml_path, "rb") as xml_file:
            files = [
                ("xml", ("cfdi.xml", xml_file, "application/octet-stream"))
            ]
            
            headers = {
                "Authorization": f"bearer {token}",
                "customid": "myCustomId",
                "Content-Type": "multipart/form-data"
            }

            # Enviar CFDI para timbrado
            response = request("POST", url_stamp, headers=headers, files=files)
            response.raise_for_status()
            
            result = response.json()
            
            # Si el timbrado fue exitoso, guardar el CFDI timbrado
            if result.get("status") == "success":
                cfdi_timbrado = result.get("data", {}).get("cfdi")
                if cfdi_timbrado:
                    output_path = Path(xml_path).parent / "cfdi_timbrado.xml"
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(cfdi_timbrado)
                    result["archivo_timbrado"] = str(output_path)
                    
            return result
            
    except Exception as e:
        return {"success": False, "error": f"Error en timbrado: {str(e)}"}
