import streamlit as st
import paramiko

# -----------------------------
# UI Setup
# -----------------------------
st.set_page_config(page_title="SSH Command Executor", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #f0f2f6; padding: 2rem;}
    .title {text-align: center; font-size: 2.5rem; color: #2c3e50; margin-bottom: 20px;}
    .command-box {border-radius: 12px; background-color: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'><div class='title'>🔐 SSH Command Executor</div>", unsafe_allow_html=True)

# -----------------------------
# SSH Authentication
# -----------------------------
def run_ssh_command(host, port, user, passwd, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=user, password=passwd)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        return output if output else error, True
    except Exception as e:
        return f"Error: {str(e)}", False

st.sidebar.header("🔑 SSH Login")
hostname = st.sidebar.text_input("Host/IP Address", "")
port = st.sidebar.number_input("Port", min_value=1, max_value=65535, value=22)
username = st.sidebar.text_input("Username", "")
password = st.sidebar.text_input("Password", type="password")

connected = False
ssh_client = None

if st.sidebar.button("Connect"):
    st.session_state['hostname'] = hostname
    st.session_state['port'] = port
    st.session_state['username'] = username
    st.session_state['password'] = password
    result, connected = run_ssh_command(hostname, port, username, password, "echo connected")
    if connected:
        st.success("✅ Connected successfully to SSH server!")
        st.session_state['connected'] = True
    else:
        st.session_state['connected'] = False
        st.error(result)

# -----------------------------
# Commands Section Only if Connected
# -----------------------------
if 'connected' in st.session_state and st.session_state['connected']:

    commands = {
        "Start Apache Server": "sudo systemctl start apache2",
        "Stop Apache Server": "sudo systemctl stop apache2",
        "Restart Apache Server": "sudo systemctl restart apache2",
        "Update System": "sudo apt update && sudo apt upgrade -y",
        "Install Nginx": "sudo apt install nginx -y",
        "Install Docker": "curl -fsSL https://get.docker.com | sh",
        "Show Current Directory": "pwd",
        "List Files": "ls -l",
        "Disk Usage": "df -h",
        "Memory Usage": "free -h",
        "Check Uptime": "uptime",
        "Show Logged In Users": "who",
        "Show System Info": "uname -a",
        "Show Running Processes": "top -b -n1 | head -20",
        "Create New Directory": "mkdir new_folder",
        "Remove Directory": "rm -r new_folder",
        "Check Active Ports": "ss -tuln",
        "Show IP Address": "ip a",
        "Ping Google": "ping -c 4 google.com",
        "Check Apache Status": "sudo systemctl status apache2",
        "List Installed Packages": "dpkg -l",
        "Reboot System": "sudo reboot",
        "Shutdown System": "sudo shutdown now",
        "Install Git": "sudo apt install git -y",
        "Check Firewall Status": "sudo ufw status"
    }

    st.markdown("### ⚙️ Select a Command to Run")
    selected_command = st.selectbox("Choose a command:", list(commands.keys()))
    custom_command = st.text_input("Or enter your own command:", "")

    final_command = custom_command.strip() if custom_command else commands[selected_command]

    if st.button("Run Command"):
        st.markdown("#### 📋 Command Output")
        with st.spinner("Executing SSH command..."):
            output, _ = run_ssh_command(
                st.session_state['hostname'],
                st.session_state['port'],
                st.session_state['username'],
                st.session_state['password'],
                final_command
            )
            st.code(output)

else:
    st.info("🔒 Please connect to a Linux system using valid SSH credentials from the sidebar to begin.")

st.markdown("</div>", unsafe_allow_html=True)
