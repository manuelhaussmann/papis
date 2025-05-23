#! /usr/bin/env bash
# papis-short-help: Email a paper to a friend.
# Copyright © 2017 Alejandro Gallo. GPLv3

if [[ $1 = "-h" ]]; then
  echo "Email a paper to a friend"
  cat <<EOF
Usage: papis output_folder
EOF
  exit 0
fi

folder_name="$1"
zip_name="${folder_name}.zip"
mail_agent=mutt

papis -l ${PAPIS_LIB} export --folder --out "${folder_name}"
if [[ ! -e ${folder_name} ]]; then
  echo "${folder_name} does not exist, exiting..."
  exit 1
fi

echo "Zipping folder (${folder_name} => ${zip_name})"
zip -r "${zip_name}" "${folder_name}"

${mail_agent} -a "${zip_name}"
