import requests
import webbrowser

# Configura estos valores con los de tu aplicación
APP_KEY = 'sb5qajyfxpx6o36'  # Reemplaza con tu App Key
APP_SECRET = 'u7eledbg2ft8ax2'  # Reemplaza con tu App Secret
REDIRECT_URI = 'http://localhost'

# Paso 1: Redirigir al usuario a la página de autorización de Dropbox
auth_url = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&response_type=code&redirect_uri={REDIRECT_URI}&token_access_type=offline'
print(f"Abriendo navegador para autorización. URL: {auth_url}")
webbrowser.open(auth_url)

# Paso 2: El usuario autoriza y obtiene un código
print("\nDespués de autorizar, serás redirigido a una URL como:")
print(f"{REDIRECT_URI}?code=CODIGO_DE_AUTORIZACION")
print("\nCopia el código completo de la URL (todo lo que viene después de 'code=')")
auth_code = input("Ingresa el código de autorización: ")

# Paso 3: Intercambiar el código por tokens
token_url = 'https://api.dropboxapi.com/oauth2/token'
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    'code': auth_code,
    'grant_type': 'authorization_code',
    'client_id': APP_KEY,
    'client_secret': APP_SECRET,
    'redirect_uri': REDIRECT_URI,
    "token_access_type": "offline"
}

print("\nSolicitando tokens...")
response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    tokens = response.json()
    print("\n=== TOKENS OBTENIDOS EXITOSAMENTE ===")
    print(f"Access Token: {tokens.get('access_token')}")
    print(f"Refresh Token: {tokens.get('refresh_token')}")
    print(f"Expira en: {tokens.get('expires_in')} segundos")
    
    print("\n=== INSTRUCCIONES ===")
    print("1. Guarda el refresh token en tu archivo .env")
    print("2. Dropbox podrá renovar automáticamente el access token en futuras conexiones.")
else:
    print(f"\n❌ Error al obtener tokens: {response.status_code}")
    print(response.text)

