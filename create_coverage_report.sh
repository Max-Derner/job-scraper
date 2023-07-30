#!/bin/bash

CURRENT_DIR=$(pwd | awk -F "/" '{print $NF}')
REQUIRED_DIR="job-scraper"
echo "${CURRENT_DIR}"
if [ "${CURRENT_DIR}" != "${REQUIRED_DIR}" ]; then
    echo "You need to be in the root directory of the project ${REQUIRED_DIR}"
    exit 1
fi

REPORTS_DIR="reports"
if [ ! -d "${REPORTS_DIR}" ]; then
    mkdir "${REPORTS_DIR}"
fi

ISO_DATE=$(date -I)

coverage run -m pytest -s
REPORT=$(coverage report)
echo "${REPORT}"
echo "${REPORT}" > "${REPORTS_DIR}/${ISO_DATE}-coverage_report.txt"
