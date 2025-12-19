#!/bin/sh

SERVICE_NAME="novelservice"
SERVICE_USER="novelservice"
SERVICE_PORT="39966"
INSTALL_DIR="/opt/novelservice"
TEMP_DIR="/tmp/novelservicedownload"

[ $(id -u) -ne 0 ] && echo "\033[33mPermission denied. Use 'sudo' to run this installation script.\033[0m" && exit 1

echo
echo "\033[32m------------ Start Deploying NovelService ------------\033[0m"
rm -rf "${TEMP_DIR}" && mkdir -p "${TEMP_DIR}"
rm -rf "${INSTALL_DIR}" && mkdir -p "${INSTALL_DIR}"
echo

echo ">>> \033[32mInstalling Edge Browser...\033[0m"
if [ -f "/usr/bin/microsoft-edge-stable" ]; then
    echo "\033[32mEdge browser is already installed, skip the download.\033[0m"
else
    echo "\033[32mStart downloading the Edge browser deb package...\033[0m"
    wget -O "${TEMP_DIR}/microsoft-edge-stable.deb" "https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_131.0.2903.112-1_amd64.deb" || { echo "\033[31mError: Edge package download failed.\033[0m" ; exit 1 ; }
    echo
    echo "\033[32mStart installing the Edge browser...\033[0m"
    apt install -y -q "${TEMP_DIR}/microsoft-edge-stable.deb" || { echo "\033[31mError: Edge browser installation failed.\033[0m" ; exit 1 ; }
fi
echo
echo "\033[32mStart installing Edge browser dependencies...\033[0m"
apt -f install -y -q
apt install xvfb fonts-wqy-zenhei -y -q
fc-cache -fv
echo

echo ">>> \033[32mInstalling Novel Service...\033[0m"
echo "\033[32mStart downloading the NovelService source code...\033[0m"
wget -O "${TEMP_DIR}/novelservice.tar.gz" "https://git.dancying.cn/Dancying/NovelService/archive/master.tar.gz" || { echo "\033[31mError: NovelService source code download failed.\033[0m" ; exit 1 ; }
tar -zxvf "${TEMP_DIR}/novelservice.tar.gz" -C "${INSTALL_DIR}" --strip-components=1 || { echo "\033[31mError: NovelService extraction failed.\033[0m" ; exit 1 ; }
echo
echo "\033[32mStart installing Python dependencies...\033[0m"
apt install python3-venv -y -q
python3 -m venv "${INSTALL_DIR}/.venv" || { echo "\033[31mError: Creating Python venv failed.\033[0m" ; exit 1 ; }
"${INSTALL_DIR}/.venv/bin/pip" install -r "${INSTALL_DIR}/requirements.txt" || { echo "\033[31mError: Python dependencies installation failed.\033[0m" ; exit 1 ; }
echo

echo ">>> \033[32mSetting up automatic startup...\033[0m"
id "${SERVICE_USER}" >/dev/null 2>&1 || useradd -m -s /usr/sbin/nologin "${SERVICE_USER}"
chown -R "${SERVICE_USER}":"${SERVICE_USER}" "${INSTALL_DIR}"
cat <<EOF | tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null
[Unit]
Description=NovelService
After=network.target

[Service]
User=${SERVICE_USER}
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/.venv/bin/gunicorn main:app -b 0.0.0.0:${SERVICE_PORT} -w 2
Restart=on-failure

# Network Proxy Settings
# Environment="HTTP_PROXY=http://127.0.0.1:10808"
# Environment="HTTPS_PROXY=http://127.0.0.1:10808"
# Environment="NO_PROXY=localhost,127.0.0.1,::1,internal-api.corp.com,192.168.1.0/24"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}.service"
systemctl start "${SERVICE_NAME}.service"
echo

echo "\033[32m------------ NovelService Deployment Complete ------------\033[0m"
echo "\033[32mNovelService deployed and listening on port '${SERVICE_PORT}'.\033[0m"
echo "\033[32mEditing file '/etc/systemd/system/${SERVICE_NAME}.service' allows you to configure a proxy.\033[0m"
echo "\033[32mView logs: 'sudo journalctl -f -u ${SERVICE_NAME}.service'\033[0m"
echo

