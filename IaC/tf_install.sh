TF_PARAM_OS="linux" # Change this to your OS (e.g., "linux", "windows", "darwin")
TF_PARAM_ARCH="amd64" # Change this to your architecture (e.g., "amd64", "386")

get_latest_terraform() {
    # Fetches the index.json from Terraform releases
    local index_json=$(curl -sf https://releases.hashicorp.com/terraform/index.json)

    # Extracts versions, filters out pre-releases, sorts, and gets the latest version
    local latest_version=$(echo "$index_json" | jq -r '.versions | keys | .[]' | grep -vE 'alpha|beta|rc' | sort -rV | head -1)

    # Constructs the download URL for the latest version
    local latest_url="https://releases.hashicorp.com/terraform/${latest_version}/terraform_${latest_version}_${TF_PARAM_OS}_${TF_PARAM_ARCH}.zip"

    echo "$latest_version"
}

apt update
apt install -y unzip jq wget

latest_version=$(get_latest_terraform)
latest_url="https://releases.hashicorp.com/terraform/${latest_version}/terraform_${latest_version}_${TF_PARAM_OS}_${TF_PARAM_ARCH}.zip"
wget -nv $latest_url

file_name="terraform_${latest_version}_${TF_PARAM_OS}_${TF_PARAM_ARCH}.zip"
unzip -o $file_name

mv terraform /usr/local/bin