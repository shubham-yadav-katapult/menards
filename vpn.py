from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection

# optional, use this on Linux and if you are not logged in when using nordvpn command

settings = initialize_vpn("France", "signups@codvo.ai", "C0dv0@2o23$!")  # starts nordvpn and stuff
rotate_VPN(settings)  # actually connect to server