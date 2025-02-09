# message_manager.py
from typing import Optional

def send_pretty_message(buffer, websocket_manager: Optional[object], message_type: str, message: str):
    message_prefix = ""
    if message_type == "success":
        message_prefix = "🟢"
    elif message_type == "error":
        message_prefix = "❌"
    elif message_type == "info":
        message_prefix = "ℹ️"
    elif message_type == "warning":
        message_prefix = "⚠️"
    
    # Crear el mensaje
    pretty_message = f"{message_prefix} {message}"
    
    # Agregar al buffer
    buffer.append(pretty_message)
    
    # Enviar al WebSocket si está disponible
    if websocket_manager:
        # Enviar el mensaje al WebSocket
        websocket_manager.broadcast(pretty_message)

    return pretty_message
